# Generated by Django 5.1 on 2025-05-25 19:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_cartconstructor_cook_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartconstructor',
            name='bisquit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.bisquit', verbose_name='Бисквит'),
        ),
        migrations.AddField(
            model_name='cartconstructor',
            name='decoration',
            field=models.ManyToManyField(blank=True, null=True, to='main.decoration', verbose_name='украшения'),
        ),
        migrations.AddField(
            model_name='cartconstructor',
            name='filling',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.filling', verbose_name='начинка'),
        ),
        migrations.AddField(
            model_name='cartconstructor',
            name='sprinkles',
            field=models.ManyToManyField(blank=True, null=True, to='main.sprinkles', verbose_name='посыпки'),
        ),
    ]
