# Generated by Django 5.0.1 on 2025-07-17 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rents', '0002_debt_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='amount',
            field=models.FloatField(verbose_name='Сумма долга (сум)'),
        ),
    ]
