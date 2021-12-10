from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

def phone_validator(phone_number):
    try:
        int(phone_number)
    except (ValueError, TypeError):
        raise ValidationError('Please enter a valid phone number')

    if len(phone_number)!=10:
        raise ValidationError('A valid phone number is 10 digits long, yours was too short')

    return phone_number

def insurance_validator(insurance):
    try:
        int(insurance)
    except (ValueError, TypeError):
        raise ValidationError('Please enter a valid insurance number')

    if len(insurance)!=10:
        raise ValidationError('A valid insurance number is 10 digits long, yours was too short.')

    return insurance

"""The User Model
    Every user of the system will instantiate an instance of this model
"""
class User(AbstractUser):
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    DoB = models.DateTimeField(max_length=100, null=True)
    phone_number = models.CharField(max_length=10, null=True,validators=[phone_validator])
    email = models.EmailField(max_length=100, null=True)

    def __str__(self):
        """String for representing the Model object."""
        name = self.first_name + " " + self.last_name
        return name

"""The Patient Model
    A patient inherits its properties from a User model.
"""
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    insurance_number = models.CharField(max_length=10, validators=[MinLengthValidator(10),insurance_validator], null=False)

"""The Staff Model
    A Staff inherits its properties from a User model.
"""
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=15)
    info = models.TextField(max_length=100, help_text='Personal Info',default="I am a staff member")

    def __str__(self):
        """String for representing the Model object."""
        if self.role == "Dentist":
            name = "Dr " + self.user.last_name
        elif self.role == "Assistant":
            name = "Assistant " + self.user.first_name + " " + self.user.last_name
        else:
            name = self.user.first_name + self.user.last_name

        return name



