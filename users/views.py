from django import views
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import UserCreateForm, UserUpdateForm
from .models import CustomUser

# Create your views here.


class RegisterView(views.View):
    def get(self, request: HttpRequest):
        user_create_form = UserCreateForm()

        context = {"form": user_create_form}
        return render(request, "users/register.html", context)

    def post(self, request: HttpRequest):
        user_create_form = UserCreateForm(data=request.POST)

        if user_create_form.is_valid():
            user_create_form.save()
            return redirect("users:login")
        else:
            context = {"form": user_create_form}
            return render(request, "users/register.html", context)


class LoginView(views.View):
    def get(self, request: HttpRequest):
        login_form = AuthenticationForm()

        context = {"login_form": login_form}
        return render(request, "users/login.html", context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            auth.login(request, user)

            messages.success(request, "You have successfully logged in.")
            return redirect("books:list")
        else:
            context = {"login_form": login_form}
            return render(request, "users/login.html", context)


class ProfileView(views.View, LoginRequiredMixin):
    def get(self, request: HttpRequest):
        if request.user in CustomUser.objects.all():
            context = {"user": request.user}
            return render(request, "users/profile.html", context)
        else:
            return redirect("users:register")


class LogoutView(views.View, LoginRequiredMixin):
    def get(self, request: HttpRequest):
        auth.logout(request)
        messages.info(request, "You have sucessfully logged out.")

        return redirect("books:list")


class ProfileUpdateView(views.View, LoginRequiredMixin):
    def get(self, request: HttpRequest):
        user_update_form = UserUpdateForm(instance=request.user)

        context = {"form": user_update_form}
        return render(request, "users/profile_edit.html", context)

    def post(self, request: HttpRequest):
        user_update_form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES,
        )

        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "You have successfully updated your profile.")

            return redirect("users:profile")

        context = {"form": user_update_form}
        return render(request, "users/profile_edit.html", context)
