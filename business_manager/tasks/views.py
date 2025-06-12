# from django.shortcuts import render

# from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from teams.models import Team, TeamMembership

from tasks.forms import TaskForm
from tasks.models import Task


class RequiredAdminAOrMembersOfTeamMixin(LoginRequiredMixin):
    """Доступ разрешен только членам команды и администратору"""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        team_id = kwargs.get("team_id")
        if not Team.objects.filter(
            Q(pk=team_id, creator=self.request.user) | Q(pk=team_id, members__id=self.request.user.pk)
        ).exists():
            return self.handle_no_permission()
        return response


class RequiredAdminOrManagerOfTeamMixin(LoginRequiredMixin):
    """Доступ разрешен только менеджерам команды и администратору"""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        team_id = kwargs.get("team_id")
        if not Team.objects.filter(
            Q(pk=team_id, creator=self.request.user)
            | Q(pk=team_id, members__id=self.request.user.pk, memberships__role=TeamMembership.RoleChoices.MANAGER)
        ).exists():
            return self.handle_no_permission()
        return response


class TaskListView(RequiredAdminAOrMembersOfTeamMixin, ListView):
    template_name = "tasks/task_list.html"
    queryset = Task.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        team_id = self.kwargs.get("team_id")
        return queryset.filter(team_id=team_id)


class TaskCreateView(RequiredAdminOrManagerOfTeamMixin, CreateView):
    template_name = "tasks/task_form.html"
    queryset = Task.objects.all()
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["team_id"] = self.kwargs.get("team_id")
        return kwargs

    def form_valid(self, form):
        team = get_object_or_404(Team, pk=self.kwargs.get("team_id"))
        form.save(commit=False)
        form.instance.creator = self.request.user
        form.instance.team = team
        form.save()
        return super().form_valid(form)


class TaskDetailView(RequiredAdminAOrMembersOfTeamMixin, DetailView):
    template_name = "tasks/task_detail.html"
    queryset = Task.objects.select_related("team", "creator", "assignee").all()

    def get_queryset(self):
        queryset = super().get_queryset()
        team_id = self.kwargs.get("team_id")
        return queryset.filter(team_id=team_id)


class TaskEditView(RequiredAdminOrManagerOfTeamMixin, UpdateView):
    template_name = "tasks/task_form.html"
    queryset = Task.objects.all()
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["team_id"] = self.kwargs.get("team_id")
        return kwargs


class TaskDeleteView(RequiredAdminOrManagerOfTeamMixin, DeleteView):
    queryset = Task.objects.all()
    success_url = reverse_lazy("tasks:task_list")
