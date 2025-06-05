from django.contrib import admin

from teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    list_display_links = ["name"]
