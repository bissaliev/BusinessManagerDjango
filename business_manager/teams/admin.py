from django.contrib import admin

from teams.models import Team, TeamMembership

admin.site.register(TeamMembership)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "creator"]
    list_display_links = ["name"]
