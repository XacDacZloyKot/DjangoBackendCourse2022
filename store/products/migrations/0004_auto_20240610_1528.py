# Generated by Django 3.2.25 on 2024-06-10 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0003_auto_20240531_1751'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basket',
            options={'verbose_name': 'корзина', 'verbose_name_plural': 'корзины пользователей'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'продукты', 'verbose_name_plural': 'продукты'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterField(
            model_name='basket',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Кол-во'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
