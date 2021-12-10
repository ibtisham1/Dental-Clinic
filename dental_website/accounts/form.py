from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Patient, Staff, User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.forms import Textarea

"""Validates the phone number inputted by the user"""


def phone_validator(phone_number):
    try:
        int(phone_number)
    except (ValueError, TypeError):
        raise ValidationError('Please enter only numbers')

    if len(phone_number) != 10:
        raise ValidationError('A phone number is 10 digits')

    return phone_number


"""Validates the insurance number inputted by the user"""


def insurance_validator(insurance_number):
    try:
        int(insurance_number)
    except (ValueError, TypeError):
        raise ValidationError('Your insurance number should be 10 numerical digits')
    return insurance_number


"""Validates the name inputted by the user"""


def name_validator(name):
    if name.isalpha():
        return name
    else:
        raise ValidationError('Please enter a valid name')


"""The Patient Sign Up form
    Receives Input from the user and therefore saves a new instance of Patient
"""


class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(validators=[name_validator], required=True)
    last_name = forms.CharField(validators=[name_validator], required=True)
    phone_number = forms.CharField(
        validators=[phone_validator, MinLengthValidator(10, message="Please input a 10 digit phone number")],
        required=True)
    email = forms.EmailField(required=True)
    DoB = forms.DateTimeField(input_formats=['%d-%m-%Y'],
                              widget=forms.DateTimeInput(attrs={
                                  'class': 'form-control datetimepicker-input',
                                  "placeholder": "dd-mm-yyyy"}), error_messages={
            'invalid': u'Please input your DoB in the requested format dd-mm-yy.'
        }, required=True)
    insurance_number = forms.CharField(
        validators=[MinLengthValidator(10, message='Please input a valid insurance number'), insurance_validator],
        required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        # Store all retrieved data into a new User object

        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.DoB = self.cleaned_data.get('DoB')
        user.save()

        patient = Patient.objects.create(user=user)
        patient.insurance_number = self.cleaned_data.get('insurance_number')
        patient.identity = "Patient"
        patient.save()
        return user


"""The Staff Sign Up form
    Receives Input from the user and therefore saves a new instance of Staff
"""


class StaffSignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        ('receptionist', 'Receptionist'),
        ('assistant', 'Assistant'),
        ('dentist', 'Dentist'),
    ]

    first_name = forms.CharField(validators=[name_validator], required=True)
    last_name = forms.CharField(validators=[name_validator], required=True)
    phone_number = forms.CharField(
        validators=[phone_validator, MinLengthValidator(10, message="Please input a 10 digit phonenumber")],
        required=True)
    role = forms.CharField(label='What is your role?', widget=forms.Select(choices=ROLE_CHOICES), required=True)
    email = forms.EmailField(required=True)
    DoB = forms.DateTimeField(input_formats=['%d-%m-%Y'],
                              widget=forms.DateTimeInput(attrs={
                                  'class': 'form-control datetimepicker-input',
                                  "placeholder": "dd-mm-yyyy"}), error_messages={
            'invalid': (u'Please input your DoB in the requested format dd-mm-yy.')
        })

    info = forms.CharField(label='What information would you like your patients to know?', widget=forms.Textarea(
        attrs={
            "placeholder": "Write information about your self such that the patients can see"
        }
    ))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        # Store all retrieved data into a new User object

        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.DoB = self.cleaned_data.get('DoB')
        user.save()
        staff = Staff.objects.create(user=user)
        staff.role = self.cleaned_data.get('role')
        staff.identity = "Staff"
        staff.info = self.cleaned_data.get('info')
        staff.save()
        return user


"""The Verification form
    Receives Input from the user and verifies their staff status
"""


class Verification(forms.Form):
    code = forms.CharField(max_length=20, required=True)
