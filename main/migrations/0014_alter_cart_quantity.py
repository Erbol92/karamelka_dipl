# Generated by Django 5.1 on 2024-09-04 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_products_slug_categoryproduct_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='кол-во в корзине'),
        ),
    ]
