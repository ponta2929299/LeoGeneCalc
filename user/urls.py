from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/",views.signup, name="signup"),
    path("login/",auth_views.LoginView.as_view(template_name="user/login.html"), name ="login"),
    path("logout/",auth_views.LogoutView.as_view(), name="logout"),
    path("user_info/", views.user_info, name="user_info"),
    path("user_delete", views.user_delete,name = "user_delete"),
]
