# Generated by Django 5.1 on 2024-10-17 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_bisquit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Название')),
                ('descrition', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Начинка',
                'verbose_name_plural': 'Начинки',
            },
        ),
    ]
