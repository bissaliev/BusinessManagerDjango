from django.db import models


class Team(models.Model):
    """Модель команды"""

    name = models.CharField("название команды", max_length=250, unique=True)
    slug = models.SlugField("слаг", max_length=250, unique=True)
    created_at = models.DateTimeField("Дата и время создания", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        ordering = ["name", "-created_at"]

    def __str__(self):
        return f"{self.name} | Дата создания {self.created_at:%Y-%m-%d}"
