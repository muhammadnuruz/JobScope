# Generated by Django 5.0.1 on 2025-06-21 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_companies_employees_companies_managers'),
        ('telegram_users', '0003_remove_telegramusers_employee_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramusers',
            name='favourite_companies',
            field=models.ManyToManyField(blank=True, related_name='favourited_by_users', to='companies.companies', verbose_name='Избранные компании'),
        ),
    ]
