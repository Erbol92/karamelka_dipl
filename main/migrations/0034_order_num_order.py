# Generated by Django 5.1 on 2025-01-16 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_remove_productingredients_calories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='num_order',
            field=models.IntegerField(default=0, verbose_name='№ заказа'),
        ),
    ]
