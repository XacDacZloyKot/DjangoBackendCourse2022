from django.contrib import admin

from products.admin import BasketAdmin
from users.models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)
    inlines = (
        BasketAdmin,
    )  # Для связи админок. Можно применять, если есть ForeginKey связь


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created', )
