from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from users.models import User


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            # Проверка наличия пользователя в БД
            user = auth.authenticate(username=username, password=password)
            if user:
                # Авторизация пользователя
                auth.login(request=request, user=user)
                return HttpResponseRedirect(redirect_to=reverse("index"))
    elif request.method == "GET":
        form = UserLoginForm()
    context = {"form": form}
    return render(request, template_name="users/login.html", context=context)


def registration(request):
    if request.method == "GET":
        form = UserRegistrationForm()
    elif request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегестрировались!")
            return HttpResponseRedirect(redirect_to=reverse("users:login"))
    context = {"form": form}
    return render(request, template_name="users/register.html", context=context)

@login_required
def profile(request):
    if request.method == "GET":
        # Заполняем форму данными текущего пользователя
        form = UserProfileForm(instance=request.user)
    elif request.method == "POST":
        form = UserProfileForm(
            instance=request.user, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            print("Сохраняем")
            form.save()
            return HttpResponseRedirect(redirect_to=reverse("users:profile"))
        else:
            print(form.errors)
    context = {
        "title": "Store - Профиль",
        "form": form,
        "baskets": Basket.objects.filter(user=request.user),
    }
    return render(request, "users/profile.html", context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(redirect_to=reverse("index"))
