from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import User, EmailVerification


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            "first_name": "Vanya",
            "last_name": "Ptushkin",
            "username": "User123",
            "email": "rabota@mail.ru",
            "password1": "12345678ABC",
            "password2": "12345678ABC",
        }
        self.path = reverse("users:registration")

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data["title"], "Store - Регистрация")
        self.assertTemplateUsed(response, "users/register.html")

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, data=self.data)

        # Check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # Check creating of email verification
        email_verify = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verify.exists())
        self.assertEqual(
            email_verify.first().expiration.date(),
            (now()+timedelta(hours=48)).date(),
        )

    def test_user_registration_post_error(self):
        user = User.objects.create(username=self.data['username'])
        response = self.client.post(path=self.path, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Пользователь с таким именем уже существует.", html=True)

