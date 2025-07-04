from django.contrib.auth.views import LoginView, LogoutView

from catalog.urls import app_name, urlpatterns
from users.apps import UsersConfig
from users.views import UserCreateView
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("register/", UserCreateView.as_view(template_name="users/user_form.html"), name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]
