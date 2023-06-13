from django.urls import re_path

from .views import LoginView, LogoutView, ProfileUpdateView, ProfileView, RegisterView

app_name = "users"
urlpatterns = [
    re_path(r"^register/?$", RegisterView.as_view(), name="register"),
    re_path(r"^login/?$", LoginView.as_view(), name="login"),
    re_path(r"^logout/?$", LogoutView.as_view(), name="logout"),
    re_path("^profile/?$", ProfileView.as_view(), name="profile"),
    re_path(r"^profile/edit/?$", ProfileUpdateView.as_view(), name="profile-edit"),
]
