from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User, EmailVerification


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'

# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             # Проверка наличия пользователя в БД
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 # Авторизация пользователя
#                 auth.login(request=request, user=user)
#                 return HttpResponseRedirect(redirect_to=reverse("index"))
#     elif request.method == "GET":
#         form = UserLoginForm()
#     context = {"form": form}
#     return render(request, template_name="users/login.html", context=context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = "Вы успешно зарегистрировались!"
    title = "Store - Регистрация"


# def registration(request):
#     if request.method == "GET":
#         form = UserRegistrationForm()
#     elif request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Вы успешно зарегистрировались!")
#             return HttpResponseRedirect(redirect_to=reverse("users:login"))
#     context = {"form": form}
#     return render(request, template_name="users/register.html", context=context)


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = "Store - Профиль"

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id, ))

# @login_required
# def profile(request):
#     if request.method == "GET":
#         # Заполняем форму данными текущего пользователя
#         form = UserProfileForm(instance=request.user)
#     elif request.method == "POST":
#         form = UserProfileForm(
#             instance=request.user, data=request.POST, files=request.FILES
#         )
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(redirect_to=reverse("users:profile"))
#         else:
#             print(form.errors)
#     context = {
#         "title": "Store - Профиль",
#         "form": form,
#         "baskets": Basket.objects.filter(user=request.user),
#     }
#     return render(request, "users/profile.html", context)


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Store - подтверждение электронной почты"
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        user = User.objects.get(email=kwargs.get('email'))
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(redirect_to=reverse('index'))
