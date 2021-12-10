from django import forms
from django.forms import Textarea
from django.db import transaction
from .models import Booking
from accounts.models import User, Patient, Staff
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.apps import apps
import datetime
from datetime import timedelta

"""DateInput
    This is a custom widget to display a calendar for the booking form.
"""


class DateInput(forms.DateInput):
    input_type = 'datetime-local'


"""pastPrevention
    This is a validator that ensures that a date that has already passed
    cannot be inputted for the booking.
"""


def pastPrevention(date):
    if date <= timezone.now():
        raise ValidationError("You have entered a date that has already passed")


"""PatientBooking Form
   This is the form in which patients may make a booking.
"""


class PatientBooking(forms.ModelForm):
    # The type of appointment desired.
    TYPE = [
        ('consult', 'consult'),
        ('check-up', 'check-up'),
        ('x-ray', 'x-ray'),
        ('surgery', 'surgery'),
    ]

    imp = [
        ('Low', 'Not Urgent'),
        ('Urgent', 'Urgent'),

    ]

    type = forms.CharField(label='Appointment Type', widget=forms.Select(choices=TYPE))
    importance = forms.CharField(label='Importance Level', widget=forms.Select(choices=imp))
    doctor = forms.ModelChoiceField(queryset=Staff.objects.filter(role='dentist'))
    date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'),
        validators=[pastPrevention],
    )

    class Meta():
        model = Booking
        fields = [
            'title',
            'notes',
            'importance',
            'doctor',
            'type',
            'date',

        ]
        widgets = {
            'notes': Textarea(
                attrs={
                    "placeholder": "Add information you would like your dentist to know"
                }
            ),

        }

    @transaction.atomic
    def save(self):
        booking = super().save(commit=False)
        booking.title = self.cleaned_data.get('title')
        booking.notes = self.cleaned_data.get('notes')
        booking.importance = self.cleaned_data.get('importance')

        type = self.cleaned_data.get('type')

        # Based on the type of appointment
        # A duration is estimated.
        if type == 'consult':
            length = 15
        elif type == 'check-up':
            length = 30
        elif type == 'x-ray':
            length = 45
        else:
            length = 60

        booking.length = datetime.timedelta(minutes=int(length))
        booking.date = self.cleaned_data.get('date')
        booking.doctor = self.cleaned_data.get('doctor')

        # This is the algorithm used to ensure duplicate or overlapping bookings do not occur.
        if Booking.objects.filter(doctor=booking.doctor).exclude(pk=self.instance.pk).exists():
            similar = Booking.objects.filter(doctor=booking.doctor).exclude(pk=self.instance.pk)
            start = booking.date
            end = booking.date + booking.length
            for compare in similar:
                if compare != booking:
                    initial = compare.date
                    final = compare.date + compare.length
                    if start <= final and initial <= end:
                        raise ValidationError(
                            "A similar booking time already exists start :%s   final :%s   end: %s  initial: %s" % (
                                start, final, end, initial))

        return booking




"""Assign
   This is the form used when a receptionist assigns an assistant to a booking
"""

class Assign(forms.Form):
    assistant = forms.ModelChoiceField(queryset=Staff.objects.filter(role='assistant'))
