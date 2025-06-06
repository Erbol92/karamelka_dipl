# Generated by Django 5.1 on 2024-11-20 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_products_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productingredients',
            name='calories',
        ),
        migrations.RemoveField(
            model_name='productingredients',
            name='carbohydrate',
        ),
        migrations.RemoveField(
            model_name='productingredients',
            name='fat',
        ),
        migrations.RemoveField(
            model_name='productingredients',
            name='protein',
        ),
        migrations.AddField(
            model_name='ingridients',
            name='calories',
            field=models.FloatField(default=0, verbose_name='каллории'),
        ),
        migrations.AddField(
            model_name='ingridients',
            name='carbohydrate',
            field=models.IntegerField(default=0, verbose_name='углеводы'),
        ),
        migrations.AddField(
            model_name='ingridients',
            name='fat',
            field=models.IntegerField(default=0, verbose_name='жиры'),
        ),
        migrations.AddField(
            model_name='ingridients',
            name='protein',
            field=models.IntegerField(default=0, verbose_name='белки'),
        ),
    ]
