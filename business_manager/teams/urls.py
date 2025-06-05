from django.urls import path

from teams import views

app_name = "teams"


urlpatterns = [
    path("/", views.TeamListView.as_view(), name="team_list"),
    path("create/", views.TeamCreateView.as_view(), name="team_create"),
    path("<int:pk>/edit/", views.TeamEditView.as_view(), name="team_edit"),
    path("<int:pk>/delete/", views.TeamDeleteView.as_view(), name="team_delete"),
]
