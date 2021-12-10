from django.test import TestCase
from accounts.models import User, Patient, Staff
from django.core.exceptions import ValidationError
from django.db.utils import DataError
# Create your tests here.


class UserValidationTestCases(TestCase):

    def test_invalid_DoB(self):
        with self.assertRaises(ValidationError):
            user = User.objects.create(first_name='John', last_name='Smith', DoB='hello',phone_number='0429587273'
                                       ,email='jsmith@gmail.com',username = 'jsmith', password = 'abc')

    def test_long_phone_number(self):
        with self.assertRaises(DataError):
            user = User.objects.create(first_name='John', last_name='Smith', DoB='1999-07-29',
                                       phone_number='04295872731',email='jsmith@gmail.com',
                                       username = 'jsmith', password = 'abc'
                                      )

    def test_invalid_phone_number(self):
        with self.assertRaises(ValidationError):
            user = User.objects.create(first_name='John', last_name='Smith', DoB='1999-07-29', phone_number="dsdkndsnkk",
                                       email='jsmith@gmail.com',username='jsmith',password='abcdefghij' )
            user.full_clean()

    def test_short_phone_number(self):
        with self.assertRaises(ValidationError):
            user = User.objects.create(first_name='John', last_name='Smith', DoB='1999-07-29', phone_number="039",
                                       email='jsmith@gmail.com',username='jsmith',password='032929282' )
            user.full_clean()


    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            user = User.objects.create(first_name='John', last_name='Smith', DoB='1999-07-29', phone_number="0412993884",
                                       email='jsmith',username='jsmith',password='032929282' )
            user.full_clean()

    def test_valid_user_creation(self):
        user = User.objects.create(first_name='John', last_name='Smith', DoB='1999-07-29', phone_number="0412993884",
                                       email='jsmith@gmail.com',username='jsmith',password='032929282')
        user.full_clean()
        self.assertEqual(User.objects.all().count(),1)


class PatientValidationTestCases(TestCase):
    def setUp(self):
        User.objects.create(first_name='John', last_name='Smith', DoB='1999-07-29', phone_number="0412993884",
                                   email='jsmith@gmail.com', username='jsmith', password='032929282')

    def test_invalid_insurance_number(self):
        with self.assertRaises(ValidationError):
            patient = Patient.objects.create(user=User.objects.get(first_name='John'),insurance_number='ascskksmwk')
            patient.full_clean()

    def test_long_insurance_number(self):
        with self.assertRaises(DataError):
            patient = Patient.objects.create(user=User.objects.get(first_name='John'),insurance_number='12212112111')
            patient.full_clean()

    def test_short_insurance_number(self):
        with self.assertRaises(ValidationError):
            patient = Patient.objects.create(user=User.objects.get(first_name='John'),insurance_number='122121121')
            patient.full_clean()

    def test_valid_insurance_number(self):
        patient = Patient.objects.create(user=User.objects.get(first_name='John'),insurance_number='1221211211')
        patient.full_clean()
        self.assertEqual(Patient.objects.all().count(), 1)


