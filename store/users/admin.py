from django.contrib import admin

from users.models import User
from products.admin import BasketAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', )
    inlines = (BasketAdmin, ) # Для связи админок. Можно применять, если есть ForeginKey связь
    