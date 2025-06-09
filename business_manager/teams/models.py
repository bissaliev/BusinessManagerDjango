from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Team(models.Model):
    """Модель команды"""

    name = models.CharField("название команды", max_length=250, unique=True)
    slug = models.SlugField("слаг", max_length=250, unique=True)
    created_at = models.DateTimeField("Дата и время создания", auto_now_add=True, db_index=True)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="administered_teams", verbose_name="администратор"
    )
    members = models.ManyToManyField(User, through="TeamMembership", related_name="teams", verbose_name="работники")

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        ordering = ["name", "-created_at"]

    def __str__(self):
        return f"{self.name} | Дата создания {self.created_at:%Y-%m-%d}"


class TeamMembership(models.Model):
    """Промежуточная модель для связи пользователей и команд с указанием роли и даты присоединения"""

    class RoleChoices(models.TextChoices):
        EMPLOYEE = "EM", "Сотрудник"
        MANAGER = "MG", "Менеджер"

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships", verbose_name="команда")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="team_memberships", verbose_name="пользователь"
    )
    role = models.CharField("Роль", max_length=2, choices=RoleChoices.choices, default=RoleChoices.EMPLOYEE)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата присоединения")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["team", "user"], name="unique_team_user")]

    def __str__(self):
        return f"Работник {self.user} в {self.team} с ролью {self.role}"
