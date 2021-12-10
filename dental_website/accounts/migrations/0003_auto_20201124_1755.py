# Generated by Django 2.2.5 on 2020-11-24 06:55

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_staff_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=10, null=True, validators=[accounts.models.phone_validator]),
        ),
    ]
