from django.db import models
from django.urls import reverse
from django.apps import apps

from accounts.models import User,Patient,Staff
from datetime import timedelta

# Create your models here.

"""Model representing a booking"""
class Booking(models.Model):

    title = models.CharField(max_length=20)
    notes = models.TextField(max_length=50, help_text='Booking Notes')
    id = models.TextField(max_length=10, help_text='Booking ID', primary_key=True, default=0)
    importance = models.CharField(max_length=20, help_text='Level of importance ')
    length = models.DurationField(null=True,default=timedelta())
    approved = models.BooleanField(default=False)
    date = models.DateTimeField(max_length=100,null=True)
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='Patient')
    doctor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='Doctor')
    assistant = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='Assistant')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('booking-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title
