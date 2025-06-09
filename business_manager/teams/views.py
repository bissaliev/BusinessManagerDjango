from django.core.paginator import Paginator
from django.db.models import Count, F, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from teams.forms import AddUserToTeamForm, TeamForm
from teams.models import Team, TeamMembership


class TeamCreateView(View):
    """Создание команды"""

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
    """Список команд"""

    template_name = "teams/team_list.html"
    model = Team

    def get(self, request):
        teams = self.model.objects.annotate(count_members=Count("members"))
        page_number = request.GET.get("page")
        paginator = Paginator(teams, 10)
        obj_list = paginator.get_page(page_number)
        return render(request, self.template_name, {"obj_list": obj_list})


class TeamEditView(View):
    """Редактирование данных команды"""

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


class TeamDetailView(View):
    """Детальная информация о команде"""

    template_name = "teams/team_detail.html"

    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        employees = team.members.all()
        employees = (
            TeamMembership.objects.select_related("user")
            .filter(team_id=team.id)
            .annotate(
                full_name=Concat(F("user__first_name"), Value(" "), F("user__last_name")),
            )
        )
        return render(request, self.template_name, {"team": team, "employees": employees})


class TeamDeleteView(View):
    """Удаление команды"""

    template_name = "teams/team_confirm_delete_form.html"

    def get(self, request, pk: int):
        team = get_object_or_404(Team, pk=pk)
        return render(request, self.template_name, {"team": team})

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        team.delete()
        return redirect("teams:team_list")


class AddUserToTeamView(View):
    """Добавление сотрудника в команду"""

    template_name = "teams/add_user_to_team_form.html"
    form_class = AddUserToTeamForm

    def get(self, request, pk: int):
        team = get_object_or_404(Team, pk=pk)
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "team": team})

    def post(self, request, pk: int):
        try:
            team = get_object_or_404(Team, pk=pk)
            form = self.form_class(request.POST)
            if not form.is_valid():
                raise ValueError("Invalid data")
            if TeamMembership.objects.filter(user=form.cleaned_data["user"]).exists():
                form.add_error("", "Пользователь уже зарегистрирован в команде")
                raise ValueError("Пользователь уже зарегистрирован в команде")
            form.save(commit=False)
            form.instance.team = team
            form.save()
            return redirect("teams:team_detail", team.pk)
        except ValueError:
            return render(request, self.template_name, {"form": form, "team": team})


class DeleteUserToTeamView(View):
    """Удаление сотрудника из команды"""

    form_class = AddUserToTeamForm

    def post(self, request, pk: int, user_id: int):
        emp = get_object_or_404(TeamMembership, team_id=pk, user_id=user_id)
        team_id = emp.team_id
        emp.delete()
        return redirect("teams:team_detail", team_id)
