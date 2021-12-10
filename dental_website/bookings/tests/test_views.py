from django.test import TestCase, RequestFactory
from accounts.models import User, Patient, Staff
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.urls import reverse
from accounts.views import index
from bookings.models import Booking
import datetime


class ViewsTestCases(TestCase):

    """The setup method which instantiates all the required patients,staff and bookings to be used in the testcases"""

    def setUp(self):
        self.home_url = reverse('home')
        self.staffsignup_url = reverse('staff_signup')
        self.patientsignup_url = reverse('patient_signup')
        self.addpatient_url = reverse('add-patient')
        self.staffhome_url = reverse('staff_home')

        user = User.objects.create_user(username='test1', password='a')

        user.save()

        patient = Patient.objects.create(user=user, insurance_number='1221211211')
        patient.save()

        self.user = user
        self.patient = patient

        user1 = User.objects.create_user(username='test', password='a')

        user1.save()

        Staff1 = Staff.objects.create(user=user1, role='dentist')
        Staff1.save()

        self.dentistuser = user1
        self.dentist = Staff.objects.get(user=user1)

        user2 = User.objects.create_user(username='test2', password='a')

        user2.save()

        Staff2 = Staff.objects.create(user=user2, role='assistant')
        Staff2.save()

        self.assistantuser = user2
        self.assistant = Staff.objects.get(user=user2)

        user3 = User.objects.create_user(username='test3', password='a')

        user3.save()

        Staff3 = Staff.objects.create(user=user3, role='receptionist')
        Staff3.save()

        self.receptionistuser = user3
        self.receptionist = Staff.objects.get(user=user3)

        booking = Booking.objects.create(title="thisisatitle", notes="some notes",
                                         importance='urgent', date='2020-12-01')
        booking.doctor = Staff.objects.get(role='dentist')
        booking.patient = User.objects.get(username='test1')
        booking.save()

        self.booking = booking

    def test_booking_confirmation_page(self):

        """Confirms the correct rendering of the booking confirmation page"""

        response = self.client.get(reverse('bookings:confirmation'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_confirmation.html')

    def test_booking_failed_page(self):

        """Confirms the correct rendering of the booking failure page"""

        response = self.client.get(reverse('bookings:failed'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_failed.html')

    def test_patient_bookings_list_page(self):

        """Test that a patient can see relevant bookings that have been assigned to them"""

        booking1 = Booking.objects.create(title="checker", notes="some notes",
                                          importance='urgent', date='2021-12-01', id=2)
        booking1.doctor = Staff.objects.get(role='dentist')
        booking1.patient = User.objects.get(username='test1')
        booking1.approved = True
        booking1.save()

        booking2 = Booking.objects.create(title="tester", notes="some notes",
                                          importance='urgent', date='2021-01-01', id=3)
        booking2.doctor = Staff.objects.get(role='dentist')
        booking2.patient = User.objects.get(username='test1')
        booking2.save()

        self.client.login(username='test1', password='a')
        response = self.client.get(reverse('bookings:patient-booking'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/patient_bookings.html')
        self.assertEquals(response.context['bookings'].count(), 1)
        self.assertEquals(response.context['unapproved'].count(), 2)

    def test_specific_patient_booking_page(self):

        """Ensures the correct booking details are given when a patient clicks on a specific booking
        in their booking list"""

        self.client.login(username='test1', password='a')
        response = self.client.get(reverse('bookings:patient-booking-detail', kwargs={'pk': self.booking.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/patient_bookings_detail.html')
        self.assertEquals(response.context['booking'].title, "thisisatitle")

    def test_staff_bookings_list_page(self):

        """Confirms the correct rendering of the staff bookings list page"""

        self.client.login(username='test3', password='a')
        response = self.client.get(reverse('bookings:staff-booking'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/staff_bookings.html')

    def test_dentist_bookings_list_page(self):

        """Confirms the correct context is provided for the dentist in their booking list page"""

        booking1 = Booking.objects.create(title="checker", notes="some notes",
                                          importance='urgent', date='2020-11-01', id=2)
        booking1.doctor = Staff.objects.get(role='dentist')
        booking1.patient = User.objects.get(username='test1')
        booking1.approved = True
        booking1.save()

        booking2 = Booking.objects.create(title="tester", notes="some notes",
                                          importance='urgent', date='2021-01-01', id=3)
        booking2.doctor = Staff.objects.get(role='dentist')
        booking2.patient = User.objects.get(username='test1')
        booking2.approved = True
        booking2.save()

        self.client.login(username='test', password='a')
        response = self.client.get(reverse('bookings:staff-booking'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/staff_bookings.html')
        self.assertEquals(response.context['previous'].count(), 1)
        self.assertEquals(response.context['upcoming'].count(), 1)

    def test_assistant_bookings_list_page(self):

        """Confirms the correct context is provided for the assistant in their booking list page"""

        booking1 = Booking.objects.create(title="checker", notes="some notes",
                                          importance='urgent', date='2020-11-01', id=2)
        booking1.doctor = Staff.objects.get(role='dentist')
        booking1.patient = User.objects.get(username='test1')
        booking1.approved = True
        booking1.save()

        booking2 = Booking.objects.create(title="tester", notes="some notes",
                                          importance='urgent', date='2021-01-01', id=3)
        booking2.doctor = Staff.objects.get(role='dentist')
        booking2.patient = User.objects.get(username='test1')
        booking2.approved = True
        booking2.assistant = self.assistant
        booking2.save()

        self.client.login(username='test2', password='a')
        response = self.client.get(reverse('bookings:staff-booking'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/staff_bookings.html')
        self.assertEquals(response.context['previous'].count(), 0)
        self.assertEquals(response.context['upcoming'].count(), 1)

    def test_receptionist_bookings_list_page(self):

        """Confirms the correct context is provided for the receptionist in their booking list page"""

        booking1 = Booking.objects.create(title="checker", notes="some notes",
                                          importance='urgent', date='2020-11-01', id=2)
        booking1.doctor = Staff.objects.get(role='dentist')
        booking1.patient = User.objects.get(username='test1')
        booking1.approved = True
        booking1.save()

        booking2 = Booking.objects.create(title="tester", notes="some notes",
                                          importance='urgent', date='2021-01-01', id=3)
        booking2.doctor = Staff.objects.get(role='dentist')
        booking2.patient = User.objects.get(username='test1')
        booking2.approved = True
        booking2.assistant = self.assistant
        booking2.save()

        self.client.login(username='test3', password='a')
        response = self.client.get(reverse('bookings:receptionist-list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/receptionist_bookings.html')

        self.assertEquals(response.context['previous'].count(), 1)
        self.assertEquals(response.context['upcoming'].count(), 1)
        self.assertEquals(response.context['unapproved'].count(), 1)
        self.assertEquals(response.context['role'], "receptionist")

    def test_specific_staff_booking_page(self):

        """Confirms that the correct details are provided for the specific booking chosen by a staff member"""

        self.client.login(username='test3', password='a')
        response = self.client.get(reverse('bookings:staff-booking-detail', kwargs={'pk': self.booking.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/staff_booking_detail.html')

        self.assertEquals(response.context['booking'].title, "thisisatitle")

    def test_valid_booking_form(self):

        """Confirms that a valid booking form renders the correct page"""

        data = {'title': 'chronic pain', 'notes': 'Hurts alot', 'importance': 'Urgent',
                'length': "01:00:00", "approved": True, "date": "2021-10-12T11:12", "type": "x-ray",
                "doctor": self.dentist.pk}
        response = self.client.post(reverse('bookings:Booking-View'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_invalid_booking_overlapping_form(self):

        """Confirms that an invalid booking form redirects to the failure page.
        In this circumstance the second booking is overlapping and hence will fail"""

        data = {'title': 'chronic pain', 'notes': 'Hurts alot', 'importance': 'Urgent',
                'length': "01:00:00", "approved": True, "date": "2021-08-12T11:12", "type": "x-ray",
                "doctor": self.dentist.pk}
        response = self.client.post(reverse('bookings:Booking-View'), data=data)

        self.assertEqual(response.status_code, 302)

        data1 = {'title': 'pain', 'notes': 'Hurts alot', 'importance': 'Urgent',
                'length': "01:00:00", "approved": True, "date": "2021-08-12T11:12", "type": "x-ray",
                "doctor": self.dentist.pk}
        response1 = self.client.post(reverse('bookings:Booking-View'), data=data1)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response1['Location'],'/bookings/bookingform/failure/')


    def test_invalid_past_booking_form(self):

        """Confirms that an invalid booking form entry does not redirect """

        data = {'title': 'chronic pain', 'notes': 'Hurts alot', 'importance': 'Urgent',
                'length': "01:00:00", "approved": True, "date": "2020-10-12T11:12", "type": "x-ray",
                "doctor": self.dentist.pk}
        response = self.client.post(reverse('bookings:Booking-View'), data=data)
        self.assertEqual(response.status_code, 200)

    def test_staff_valid_booking_form(self):

        """Confirms that a valid booking form made by a staff member correctly redirects """

        self.client.login(username='test3', password='a')
        data = {'title': 'chronic pain', 'notes': 'Hurts alot', 'importance': 'Urgent',
                'length': "01:00:00", "approved": True, "date": "2021-10-12T11:12", "type": "x-ray",
                "doctor": self.dentist.pk}
        response = self.client.post(reverse('bookings:create_booking', kwargs={'pk': self.patient.pk}), data=data)

        self.assertEqual(response.status_code, 302)

    def test_staff_invalid_booking_form(self):

        """Confirms that an invalid booking form made by a staff member does redirect to fail page """

        self.client.login(username='test3', password='a')
        data = {'title': 'chronic pain', 'notes': 'Hurts alot', 'importance': 'Urgent',
                'length': "01:00:00", "approved": True, "date": "2021-10-12 11:12", "type": "x-ray",
                "doctor": self.dentist.pk}
        response = self.client.post(reverse('bookings:create_booking', kwargs={'pk': self.patient.pk}), data=data)

        self.assertEqual(response.status_code, 302)

    def test_cancel_booking(self):

        """confirms that deletion of booking removes it from the database"""

        self.client.login(username='test3', password='a')

        response = self.client.get(reverse('bookings:Cancel-Booking', kwargs={'pk': self.booking.pk}))

        self.assertEqual(Booking.objects.all().count(), 0)

        self.assertEqual(response.status_code, 302)

    def test_approve_booking(self):

        """confirms that a booking is now approved when a receptionist approves the booking."""

        self.client.login(username='test3', password='a')

        self.assertFalse(Booking.objects.get(pk=self.booking.pk).approved)
        response = self.client.get(reverse('bookings:Approve-Booking', kwargs={'pk': self.booking.pk}))

        self.assertTrue(Booking.objects.get(pk=self.booking.pk).approved)

        self.assertEqual(response.status_code, 302)

    def test_edit_booking(self):

        """confirms that editing an existing booking does indeed update the values"""

        data = {'title': 'chronic pain', 'notes': 'Hurts alot', 'importance': 'Urgent',
                'length': "01:00:00", "approved": True, "date": "2021-10-12T11:12", "type": "x-ray",
                "doctor": self.dentist.pk}

        response = self.client.post(
            reverse('bookings:Edit-Booking-View', kwargs={'pk': self.booking.pk}),
            data=data)

        self.assertEqual(response.status_code, 302)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.title, 'chronic pain')

    def test_patient_medical_history_page(self):

        """Ensures the correct medical history is provided for the particular patient"""

        booking1 = Booking.objects.create(title="checker", notes="some notes",
                                          importance='urgent', date='2020-11-01', id=2)
        booking1.doctor = Staff.objects.get(role='dentist')
        booking1.patient = User.objects.get(username='test1')
        booking1.approved = True
        booking1.save()

        booking2 = Booking.objects.create(title="tester", notes="some notes",
                                          importance='urgent', date='2020-01-01', id=3)
        booking2.doctor = Staff.objects.get(role='dentist')
        booking2.patient = User.objects.get(username='test1')
        booking2.approved = True
        booking2.assistant = self.assistant
        booking2.save()

        self.client.login(username='test3', password='a')
        response = self.client.get(reverse('bookings:patient-medical', kwargs={'pk': self.user.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/medical_history.html')
        self.assertEquals(response.context['booking_list'][0].title, "checker")
        self.assertEquals(response.context['booking_list'][1].title, "tester")

    def test_patient_upcoming_bookings_page(self):

        """Ensures the correct bookings are in the upcoming bookings page """

        booking1 = Booking.objects.create(title="checker", notes="some notes",
                                          importance='urgent', date='2022-11-01', id=2)
        booking1.doctor = Staff.objects.get(role='dentist')
        booking1.patient = User.objects.get(username='test1')
        booking1.approved = True
        booking1.save()

        booking2 = Booking.objects.create(title="tester", notes="some notes",
                                          importance='urgent', date='2022-01-01', id=3)
        booking2.doctor = Staff.objects.get(role='dentist')
        booking2.patient = User.objects.get(username='test1')
        booking2.approved = True
        booking2.assistant = self.assistant
        booking2.save()

        self.client.login(username='test3', password='a')
        response = self.client.get(reverse('bookings:patient-upcoming', kwargs={'pk': self.user.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/upcoming_bookings.html')
        self.assertEquals(response.context['booking_list'][0].title, "checker")
        self.assertEquals(response.context['booking_list'][1].title, "tester")

    def test_assign_booking(self):

        """Ensures an assistant is assigned to a booking by a receptionist"""

        data = {"assistant": self.assistant.pk}
        self.assertEqual(self.booking.assistant, None)
        response = self.client.post(
            reverse('bookings:assign', kwargs={'pk': self.booking.pk}),
            data=data)

        self.booking.refresh_from_db()
        self.assertNotEqual(self.booking.assistant, None)

        self.assertEqual(response.status_code, 302)
