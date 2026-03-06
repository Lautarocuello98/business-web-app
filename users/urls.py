from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import LoginForm

app_name = "users"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logged_out.html"),
        name="logout",
    ),
]

