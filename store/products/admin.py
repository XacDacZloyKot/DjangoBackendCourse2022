from django.contrib import admin

from products.models import Basket, ProductCategory, Product

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "category")  # Отображение полей
    fields = (
        "name",
        "description",
        ("price", "quantity"),
        "image",
        "category",
        "stripe_product_price_id",
    )  # Поля самого товара
    readonly_fields = ("description",)  # Поля только для чтения
    search_fields = ("name", "price")  # По чему можем искать
    ordering = ("name",)


# TabularInline нужен связи этой модели с другой в админке
class BasketAdmin(admin.TabularInline):
    model = Basket
    readonly_fields = ("create_timestamp",)
    fields = ("product", "quantity", "create_timestamp")
    extra = 1  # Дополнительные поля в админке для создания
