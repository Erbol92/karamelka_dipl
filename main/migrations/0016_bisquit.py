# Generated by Django 5.1 on 2024-09-11 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_cart_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bisquit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Название')),
                ('descrition', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Бисквит',
                'verbose_name_plural': 'Бисквиты',
            },
        ),
    ]
