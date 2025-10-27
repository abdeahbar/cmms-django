from django.urls import path

from .views import AdminDashboardView, HomeView, RegisterView, UserLoginView, UserLogoutView

app_name = "users"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("admin-dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
]
