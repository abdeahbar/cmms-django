from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import LoginForm, RegisterForm

User = get_user_model()


class HomeView(TemplateView):
    template_name = "users/home.html"


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy("users:admin-dashboard")
        return reverse_lazy("users:home")


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Compte cree avec succes. Bienvenue !")
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy("users:admin-dashboard")
        return reverse_lazy("users:home")


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "users/admin_dashboard.html"

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Acces refuse : section reservee au personnel.")
            return redirect("users:home")
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "users_count": User.objects.count(),
                "staff_count": User.objects.filter(is_staff=True).count(),
                "groups": Group.objects.all(),
            }
        )
        return context
