# Generated by Django 5.1 on 2024-11-07 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_cartconstructor_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bisquit',
            name='price',
            field=models.FloatField(default=0, verbose_name='цена за кг'),
        ),
        migrations.AddField(
            model_name='filling',
            name='price',
            field=models.FloatField(default=0, verbose_name='цена за кг'),
        ),
        migrations.AlterField(
            model_name='cartconstructor',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='количество'),
        ),
    ]
