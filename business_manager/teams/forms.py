from django import forms

from teams.models import Team, TeamMembership


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "slug")


class AddUserToTeamForm(forms.ModelForm):
    class Meta:
        model = TeamMembership
        fields = ("user", "role")
