# Generated by Django 5.1 on 2025-02-22 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_order_num_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartconstructor',
            name='uniq_id',
        ),
    ]
