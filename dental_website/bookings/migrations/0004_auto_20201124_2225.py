# Generated by Django 2.2.5 on 2020-11-24 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_auto_20201124_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='notes',
            field=models.TextField(help_text='Booking Notes', max_length=50),
        ),
    ]