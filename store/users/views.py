from django.shortcuts import render
from users.forms import UserLoginForm
from users.models import User


def login(request):
    context = {'form': UserLoginForm()}
    return render(request, template_name='users/login.html', context=context)


def registration(request):
    return render(request, template_name='users/register.html')
