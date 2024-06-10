from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(
        upload_to='users_images',
        null=True,
        blank=True,
        verbose_name='Фото'
    )
    is_verified_email = models.BooleanField(default=False, verbose_name="Верификация почты")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True, verbose_name="ID")
    user = models.ForeignKey(to=User,on_delete=models.CASCADE, verbose_name="Пользователь")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    expiration = models.DateTimeField(verbose_name="Дата удаления")

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'code': self.code, 'email': self.user.email})
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Подтверждение учётной записи для {self.user.username}"
        message = "Для подтверждения учётной записи для {} перейдите по ссылке: {}".format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False


    class Meta:
        verbose_name = 'Верификация почты'
        verbose_name_plural = 'Верификаций почты'


