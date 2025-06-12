from django import forms
from django.contrib.auth import get_user_model

from tasks.models import Task

User = get_user_model()


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TaskForm(forms.ModelForm):
    assignee = UserModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Выберите исполнителя",
        label="Исполнитель",
    )

    def __init__(self, *args, **kwargs):
        team_id = kwargs.pop("team_id")
        super().__init__(*args, **kwargs)
        self.fields["assignee"].queryset = self.fields["assignee"].queryset.filter(teams__id__in=[team_id])

    class Meta:
        model = Task
        exclude = ("creator", "team")
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }
