# Generated by Django 5.1 on 2024-08-21 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_categoryproduct_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryproduct',
            name='slug',
            field=models.SlugField(null=True, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_cat', to='main.categoryproduct', verbose_name='категория'),
        ),
    ]
