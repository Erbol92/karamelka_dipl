# Generated by Django 5.1 on 2024-08-21 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_products_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='slug',
        ),
        migrations.AddField(
            model_name='categoryproduct',
            name='slug',
            field=models.SlugField(null=True, unique=True, verbose_name='URL'),
        ),
    ]
