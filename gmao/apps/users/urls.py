from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import AdminDashboardView, HomeView, RegisterView, UserLoginView

app_name = "users"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="users:home"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("admin-dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
]
