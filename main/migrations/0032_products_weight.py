# Generated by Django 5.1 on 2024-11-20 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_alter_comment_options_comment_moderated'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='вес продукта'),
        ),
    ]