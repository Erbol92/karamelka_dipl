# Generated by Django 5.1 on 2025-01-16 10:09

import user_manager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0003_userproxy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=16, null=True, verbose_name='№ тел.'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=user_manager.models.Profile.image_path, verbose_name='фото'),
        ),
    ]
