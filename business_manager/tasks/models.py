from django.contrib.auth import get_user_model
from django.db import models
from teams.models import Team

from tasks.validators import validate_datetime

User = get_user_model()


class Task(models.Model):
    """Модель задач"""

    class Status(models.TextChoices):
        OPEN = "OPEN", "открыто"
        IN_PROGRESS = "IN_PROGRESS", "в работе"
        COMPLETED = "COMPLETED", "выполнено"

    title = models.CharField("Заголовок", max_length=250)
    description = models.TextField("Описание")
    start_time = models.DateTimeField("Начало задачи", db_index=True, validators=[validate_datetime])
    end_time = models.DateTimeField("Конец задачи", db_index=True, validators=[validate_datetime])
    status = models.CharField("Статус задачи", max_length=15, choices=Status.choices, default=Status.OPEN)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="set_tasks", verbose_name="Инициатор задачи"
    )
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assigned_tasks", verbose_name="Исполнитель задачи"
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_tasks", verbose_name="Команда")
    created_at = models.DateTimeField("Дата создания задачи", auto_now_add=True)
    updated_at = models.DateTimeField("Дата последнего обновления", auto_now=True)

    def __str__(self):
        return f"Task({self.title})"

    class Meta:
        ordering = ["-start_time", "-end_time"]
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
