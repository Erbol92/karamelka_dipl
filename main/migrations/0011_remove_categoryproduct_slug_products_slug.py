# Generated by Django 5.1 on 2024-08-21 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_categoryproduct_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryproduct',
            name='slug',
        ),
        migrations.AddField(
            model_name='products',
            name='slug',
            field=models.SlugField(null=True, unique=True, verbose_name='URL'),
        ),
    ]
