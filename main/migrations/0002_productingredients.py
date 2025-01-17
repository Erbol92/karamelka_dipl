# Generated by Django 5.1 on 2024-08-20 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductIngredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ingridient', models.CharField(max_length=50, verbose_name='название ингридиента')),
                ('amount', models.FloatField(default=0, verbose_name='кол-во')),
                ('unit', models.CharField(choices=[('things', 'шт.'), ('gram', 'грамм'), ('tsn', 'ч.л.'), ('tbsn', 'ст.л.')], max_length=10, verbose_name='ед. изм.')),
                ('protein', models.FloatField(default=0, verbose_name='белки')),
                ('fat', models.FloatField(default=0, verbose_name='жиры')),
                ('carbohydrate', models.FloatField(default=0, verbose_name='углеводы')),
                ('calories', models.FloatField(default=0, verbose_name='каллории')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products', verbose_name='продукт')),
            ],
        ),
    ]
