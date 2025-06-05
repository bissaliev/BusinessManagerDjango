from django.urls import path

from users.views import ProfileDetailView, RegisterView, UpdateProfileView, UserLoginView, UserLogoutView

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("<int:pk>/", ProfileDetailView.as_view(), name="profile"),
    path("<int:pk>/edit/", UpdateProfileView.as_view(), name="edit_profile"),
]
