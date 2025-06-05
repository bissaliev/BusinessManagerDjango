from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from teams.forms import TeamForm
from teams.models import Team


class TeamCreateView(View):
    form_class = TeamForm
    template_name = "teams/team_form.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        return render(request, self.template_name, {"form": form})


class TeamListView(View):
    template_name = "teams/team_list.html"
    model = Team

    def get(self, request):
        teams = self.model.objects.all()
        page_number = request.GET.get("page")
        paginator = Paginator(teams, 10)
        obj_list = paginator.get_page(page_number)
        return render(request, self.template_name, {"obj_list": obj_list})


class TeamEditView(View):
    form_class = TeamForm
    template_name = "teams/team_form.html"

    def get(self, request, pk: int):
        team = get_object_or_404(Team, pk=pk)
        form = self.form_class(instance=team)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        form = self.form_class(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect("teams:team_list")
        return render(request, self.template_name, {"form": form})


class TeamDeleteView(View):
    template_name = "teams/team_confirm_delete_form.html"

    def get(self, request, pk: int):
        team = get_object_or_404(Team, pk=pk)
        return render(request, self.template_name, {"team": team})

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        team.delete()
        return redirect("teams:team_list")
