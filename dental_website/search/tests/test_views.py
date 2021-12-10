from django.test import TestCase, RequestFactory
from accounts.models import User, Patient, Staff
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.urls import reverse
from accounts.views import index
from bookings.models import Booking
import datetime
from django.http import QueryDict


class ViewsTestCases(TestCase):
    def setUp(self):
        """Set up method to create all patients,staff and bookings required for the test cases"""

        user = User.objects.create_user(username='test1', password='a')
        user.first_name = "Peter"
        user.last_name = "Gold"
        user.save()

        patient = Patient.objects.create(user=user, insurance_number='1221211211')
        patient.save()

        self.user = user
        self.patient = patient

        user1 = User.objects.create_user(username='test', password='a')
        user1.first_name = "Steve"
        user1.last_name = "Smith"
        user1.save()

        Staff1 = Staff.objects.create(user=user1, role='dentist')
        Staff1.save()

        self.dentistuser = user1
        self.dentist = Staff.objects.get(user=user1)

        user2 = User.objects.create_user(username='test2', password='a')
        user2.first_name = "Jane"
        user2.last_name = "Mikal"
        user2.save()

        Staff2 = Staff.objects.create(user=user2, role='assistant')
        Staff2.save()

        self.assistantuser = user2
        self.assistant = Staff.objects.get(user=user2)

        user3 = User.objects.create_user(username='test3', password='a')
        user3.first_name = "Brad"
        user3.last_name = "Johns"
        user3.save()

        Staff3 = Staff.objects.create(user=user3, role='receptionist')
        Staff3.save()

        self.receptionistuser = user3
        self.receptionist = Staff.objects.get(user=user3)

        booking = Booking.objects.create(title="thisisatitle", notes="some notes",
                                         importance='urgent', date='2020-12-01')
        booking.doctor = Staff1
        booking.patient = User.objects.get(username='test1')
        booking.save()
        self.booking = booking

        booking1 = Booking.objects.create(title="pain", notes="some notes",
                                          importance='urgent', date='2021-12-01', id=3)
        booking1.doctor = Staff1
        booking1.patient = User.objects.get(username='test1')
        booking1.save()
        self.booking1 = booking1

        user5 = User.objects.create_user(username='dentist2', password='a')
        user5.first_name = "David"
        user5.last_name = "Lee"
        user5.save()

        Staff5 = Staff.objects.create(user=user5, role='dentist')
        Staff5.save()

        self.dentist2 = Staff5
        self.dentistuser2 = user5

        booking2 = Booking.objects.create(title="chronic pain", notes="some notes",
                                          importance='urgent', date='2022-12-01', id=4)
        booking2.doctor = Staff5
        booking2.patient = User.objects.get(username='test1')
        booking2.save()
        self.booking2 = booking1


    def test_search_booking_by_title_receptionist_page(self):
        """Testing the booking search bar by using title for a receptionist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_receptionist'),
            filter='q', value='thisisatitle')

        self.client.login(username='test3', password='a')

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_receptionist.html')
        self.assertEquals(response.context['role'], "receptionist")
        self.assertEquals(response.context['query'], "thisisatitle")
        self.assertEquals(response.context['object_list'][0].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_dentist_first_name_receptionist_page(self):
        """Testing the booking search bar by using dentist's firstname for a receptionist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_receptionist'),
            filter='q', value='Steve')

        self.client.login(username='test3', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_receptionist.html')
        self.assertEquals(response.context['role'], "receptionist")
        self.assertEquals(response.context['query'], "Steve")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'][1].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 2)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_dentist_last_name_receptionist_page(self):
        """Testing the booking search bar by using dentist's lastname for a receptionist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_receptionist'),
            filter='q', value='Smith')

        self.client.login(username='test3', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_receptionist.html')
        self.assertEquals(response.context['role'], "receptionist")
        self.assertEquals(response.context['query'], "Smith")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'][1].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 2)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_assistant_first_name_receptionist_page(self):
        """Testing the booking search bar by using assistant's firstname for a receptionist"""

        self.booking1.assistant = self.assistant
        self.booking1.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_receptionist'),
            filter='q', value='Jane')

        self.client.login(username='test3', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_receptionist.html')
        self.assertEquals(response.context['role'], "receptionist")
        self.assertEquals(response.context['query'], "Jane")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_assistant_last_name_receptionist_page(self):
        """Testing the booking search bar by using assistant's last name for a receptionist"""

        self.booking1.assistant = self.assistant
        self.booking1.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_receptionist'),
            filter='q', value='Mikal')

        self.client.login(username='test3', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_receptionist.html')
        self.assertEquals(response.context['role'], "receptionist")
        self.assertEquals(response.context['query'], "Mikal")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)


    def test_search_booking_by_patient_first_name_receptionist_page(self):
        """Testing the booking search bar by using patient's first name for a receptionist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_receptionist'),
            filter='q', value='Peter')

        self.client.login(username='test3', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_receptionist.html')
        self.assertEquals(response.context['role'], "receptionist")
        self.assertEquals(response.context['query'], "Peter")
        self.assertEquals(response.context['object_list'][0].title, "chronic pain")
        self.assertEquals(response.context['object_list'][1].title, "pain")
        self.assertEquals(response.context['object_list'][2].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 3)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_patient_last_name_receptionist_page(self):
        """Testing the booking search bar by using patient's last name for a receptionist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_receptionist'),
            filter='q', value='Gold')

        self.client.login(username='test3', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_receptionist.html')
        self.assertEquals(response.context['role'], "receptionist")
        self.assertEquals(response.context['query'], "Gold")
        self.assertEquals(response.context['object_list'][0].title, "chronic pain")
        self.assertEquals(response.context['object_list'][1].title, "pain")
        self.assertEquals(response.context['object_list'][2].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 3)
        self.assertEquals(Booking.objects.all().count(), 3)



    def test_search_booking_by_title_dentist_page(self):
        """Testing the booking search bar by using title for a dentist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='thisisatitle')

        self.client.login(username='test', password='a')

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "dentist")
        self.assertEquals(response.context['query'], "thisisatitle")
        self.assertEquals(response.context['object_list'][0].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_dentist_first_name_dentist_page(self):
        """Testing the booking search bar by using dentist's firstname for a dentist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Steve')

        self.client.login(username='test', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "dentist")
        self.assertEquals(response.context['query'], "Steve")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'][1].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 2)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_dentist_last_name_dentist_page(self):
        """Testing the booking search bar by using dentist's lastname for a dentist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Smith')

        self.client.login(username='test', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "dentist")
        self.assertEquals(response.context['query'], "Smith")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'][1].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 2)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_assistant_first_name_dentist_page(self):
        """Testing the booking search bar by using assistant's firstname for a dentist"""

        self.booking1.assistant = self.assistant
        self.booking1.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Jane')

        self.client.login(username='test', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "dentist")
        self.assertEquals(response.context['query'], "Jane")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_assistant_last_name_dentist_page(self):
        """Testing the booking search bar by using assistant's last name for a dentist"""

        self.booking1.assistant = self.assistant
        self.booking1.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Mikal')

        self.client.login(username='test', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "dentist")
        self.assertEquals(response.context['query'], "Mikal")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)


    def test_search_booking_by_patient_first_name_dentist_page(self):
        """Testing the booking search bar by using patient's first name for a dentist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Peter')

        self.client.login(username='test', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "dentist")
        self.assertEquals(response.context['query'], "Peter")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'][1].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 2)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_patient_last_name_dentist_page(self):
        """Testing the booking search bar by using patient's last name for a dentist"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Gold')

        self.client.login(username='test', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "dentist")
        self.assertEquals(response.context['query'], "Gold")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'][1].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 2)
        self.assertEquals(Booking.objects.all().count(), 3)



    def test_search_booking_by_title_assistant_page(self):
        """Testing the booking search bar by using title for an assistant"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='thisisatitle')

        self.client.login(username='test2', password='a')

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "assistant")
        self.assertEquals(response.context['query'], "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 0)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_dentist_first_name_assistant_page(self):
        """Testing the booking search bar by using dentist's firstname for an assistant"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Steve')

        self.client.login(username='test2', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "assistant")
        self.assertEquals(response.context['query'], "Steve")
        self.assertEquals(response.context['object_list'].count(), 0)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_dentist_last_name_assistant_page(self):
        """Testing the booking search bar by using dentist's lastname for an assistant"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Smith')

        self.client.login(username='test2', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "assistant")
        self.assertEquals(response.context['query'], "Smith")
        self.assertEquals(response.context['object_list'].count(), 0)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_assistant_first_name_assistant_page(self):
        """Testing the booking search bar by using assistant's firstname for an assistant"""

        self.booking1.assistant = self.assistant
        self.booking1.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Jane')

        self.client.login(username='test2', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "assistant")
        self.assertEquals(response.context['query'], "Jane")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_assistant_last_name_assistant_page(self):
        """Testing the booking search bar by using assistant's last name for an assistant"""

        self.booking1.assistant = self.assistant
        self.booking1.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Mikal')

        self.client.login(username='test2', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "assistant")
        self.assertEquals(response.context['query'], "Mikal")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)


    def test_search_booking_by_patient_first_name_assistant_page(self):
        """Testing the booking search bar by using patient's first name for an assistant"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Peter')

        self.client.login(username='test2', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "assistant")
        self.assertEquals(response.context['query'], "Peter")
        self.assertEquals(response.context['object_list'].count(), 0)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_patient_last_name_assistant_page(self):
        """Testing the booking search bar by using patient's last name for an assistant"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_staff'),
            filter='q', value='Gold')

        self.client.login(username='test2', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff.html')
        self.assertEquals(response.context['role'], "assistant")
        self.assertEquals(response.context['query'], "Gold")
        self.assertEquals(response.context['object_list'].count(), 0)
        self.assertEquals(Booking.objects.all().count(), 3)



    def test_search_booking_by_title_patient_page(self):
        """Testing the booking search bar by using title for a patient"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_patient'),
            filter='q', value='thisisatitle')

        self.client.login(username='test1', password='a')

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_patient.html')
        self.assertEquals(response.context['query'], "thisisatitle")
        self.assertEquals(response.context['object_list'][0].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_dentist_first_name_patient_page(self):
        """Testing the booking search bar by using dentist's firstname for a patient"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_patient'),
            filter='q', value='Steve')

        self.client.login(username='test1', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_patient.html')
        self.assertEquals(response.context['query'], "Steve")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'][1].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 2)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_dentist_last_name_patient_page(self):
        """Testing the booking search bar by using dentist's lastname for a patient"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_patient'),
            filter='q', value='Smith')

        self.client.login(username='test1', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_patient.html')
        self.assertEquals(response.context['query'], "Smith")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'][1].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 2)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_assistant_first_name_patient_page(self):
        """Testing the booking search bar by using assistant's firstname for a patient"""

        self.booking1.assistant = self.assistant
        self.booking1.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_patient'),
            filter='q', value='Jane')

        self.client.login(username='test1', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_patient.html')
        self.assertEquals(response.context['query'], "Jane")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_assistant_last_name_patient_page(self):
        """Testing the booking search bar by using assistant's last name for a patient"""

        self.booking1.assistant = self.assistant
        self.booking1.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_patient'),
            filter='q', value='Mikal')

        self.client.login(username='test1', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_patient.html')
        self.assertEquals(response.context['query'], "Mikal")
        self.assertEquals(response.context['object_list'][0].title, "pain")
        self.assertEquals(response.context['object_list'].count(), 1)
        self.assertEquals(Booking.objects.all().count(), 3)


    def test_search_booking_by_patient_first_name_patient_page(self):
        """Testing the booking search bar by using patient's first name for a patient"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_patient'),
            filter='q', value='Peter')

        self.client.login(username='test1', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_patient.html')
        self.assertEquals(response.context['query'], "Peter")
        self.assertEquals(response.context['object_list'][0].title, "chronic pain")
        self.assertEquals(response.context['object_list'][1].title, "pain")
        self.assertEquals(response.context['object_list'][2].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 3)
        self.assertEquals(Booking.objects.all().count(), 3)

    def test_search_booking_by_patient_last_name_patient_page(self):
        """Testing the booking search bar by using patient's last name for a patient"""

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_patient'),
            filter='q', value='Gold')

        self.client.login(username='test1', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_patient.html')
        self.assertEquals(response.context['query'], "Gold")
        self.assertEquals(response.context['object_list'][0].title, "chronic pain")
        self.assertEquals(response.context['object_list'][1].title, "pain")
        self.assertEquals(response.context['object_list'][2].title, "thisisatitle")
        self.assertEquals(response.context['object_list'].count(), 3)
        self.assertEquals(Booking.objects.all().count(), 3)



    def test_staff_patient_search_by_first_name_page(self):

        """Testing the patient search bar by using first_name for a staff member"""

        user = User.objects.create_user(username='tester', password='a')
        user.first_name="Jasper"
        user.save()
        patient = Patient.objects.create(user=user, insurance_number='1221211211')
        patient.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_people'),
            filter='q', value='Jasper')

        self.client.login(username='test3', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff_patient.html')
        self.assertEquals(response.context['query'], "Jasper")
        self.assertEquals(response.context['search_list'][0].first_name,"Jasper")
        self.assertEquals(response.context['search_list'].count(),1)
        self.assertEquals(Patient.objects.all().count(),2)


    def test_staff_patient_search_by_last_name_page(self):

        """Testing the patient search bar by using last_name for a staff member"""

        user = User.objects.create_user(username='tester', password='a')
        user.last_name="Banks"
        user.save()
        patient = Patient.objects.create(user=user, insurance_number='1221211211')
        patient.save()

        url = '{url}?{filter}={value}'.format(
            url=reverse('search_people'),
            filter='q', value='Banks')

        self.client.login(username='test3', password='a')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_staff_patient.html')
        self.assertEquals(response.context['query'], "Banks")
        self.assertEquals(response.context['search_list'][0].last_name,"Banks")
        self.assertEquals(response.context['search_list'].count(),1)
        self.assertEquals(Patient.objects.all().count(),2)

