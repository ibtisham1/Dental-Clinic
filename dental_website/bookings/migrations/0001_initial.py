# Generated by Django 2.2.5 on 2020-11-18 10:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('notes', models.TextField(help_text='Booking Notes', max_length=1000)),
                ('id', models.TextField(default=0, help_text='Booking ID', max_length=10, primary_key=True, serialize=False)),
                ('importance', models.TextField(help_text='Level of importance ', max_length=20)),
                ('length', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('approved', models.BooleanField(default=False)),
                ('date', models.DateTimeField(max_length=100, null=True)),
                ('assistant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Assistant', to='accounts.Staff')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Doctor', to='accounts.Staff')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
