from django.test import TestCase
from bookings.models import Booking
from django.core.exceptions import ValidationError
from django.db.utils import DataError
# Create your tests here.


class BookingValidationTestCases(TestCase):

    def test_long_title(self):
        with self.assertRaises(DataError):
            booking = Booking.objects.create(title="a"*30,notes="i am sick",importance='urgent',date='2020-12-01')
            booking.full_clean()

    def test_invalid_date(self):
        with self.assertRaises(ValidationError):
            booking = Booking.objects.create(title="thisisatitle", notes="a"*10,
                                             importance='urgent', date='asas')
            booking.full_clean()

    def test_valid_booking(self):

        booking = Booking.objects.create(title="thisisatitle", notes="some notes",
                                         importance='urgent', date='2020-12-01')
        booking.full_clean()

        self.assertEquals(Booking.objects.all().count(),1)

