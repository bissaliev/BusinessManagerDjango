from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from users.forms import ProfileForm, RegisterForm

User = get_user_model()


class AdminAndOwnerRequired(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        user_to_edit = self.get_object()
        if not (request.user.is_superuser or user_to_edit == request.user):
            return self.handle_no_permission()
        return response


class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(LogoutView): ...


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = RegisterForm


class UpdateProfileView(AdminAndOwnerRequired, UpdateView):
    template_name = "users/edit_profile.html"
    form_class = ProfileForm
    model = User

    def get_success_url(self) -> str:
        return reverse("users:profile", args=[self.object.pk])


class ProfileDetailView(AdminAndOwnerRequired, DetailView):
    template_name = "users/profile.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.object.assigned_tasks.all()
        context["tasks"] = tasks
        return context
