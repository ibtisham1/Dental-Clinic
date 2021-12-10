from django.test import TestCase, RequestFactory
from accounts.models import User, Patient, Staff
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.urls import reverse
from accounts.views import index
from bookings.models import Booking
from accounts.form import PatientSignUpForm


# Create your tests here.


class ViewsTestCases(TestCase):
    def setUp(self):

        """The set up method where patients,staffs are created and urls are stored"""

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

    def test_not_authenticated_homepage(self):

        """Test whether the correct page is rendered if the user is not authenticated"""

        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_dentist_authenticated_homepage(self):

        """Test whether a dentist who has logged in is directed to the correct homepage"""

        self.client.login(username='test', password='a')
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'staff_home.html')

    def test_receptionist_authenticated_homepage(self):

        """Test whether a receptionist who has logged in is directed to the correct homepage"""

        self.client.login(username='test3', password='a')
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'staff_home.html')

    def test_assistant_authenticated_homepage(self):

        """Test whether an assistant who has logged in is directed to the correct homepage"""

        self.client.login(username='test2', password='a')
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'staff_home.html')

    def test_patient_signup_form(self):

        """Test whether a patient who has filled in the sign up form correctly has been added to the database"""

        data = {'first_name': "tester", 'last_name': "testing", 'DoB': '28-12-1999',
                'phone_number': "0412993884", 'email': 'jsmith@gmail.com',
                'username': 'jsmith', 'password1': 'homeplus123', 'insurance_number': "0429183747",
                'password2': 'homeplus123'}

        response = self.client.post(self.patientsignup_url, data=data, follow=True)

        self.user.refresh_from_db()
        self.assertTrue(User.objects.filter(first_name="tester").exists())

    def test_staff_signup_form(self):

        """Test whether a staff who has filled in the sign up form correctly has been added to the database"""

        data = {'first_name': "tester", 'last_name': "testing", 'DoB': '28-12-1999',
                'phone_number': "0412993884", 'email': 'jsmith@gmail.com',
                'username': 'jsmith', 'password1': 'homeplus123',
                'password2': 'homeplus123', 'role': "dentist", 'info': "someinfo"}

        response = self.client.post(self.staffsignup_url, data=data, follow=True)

        self.user.refresh_from_db()
        self.assertTrue(User.objects.filter(first_name="tester").exists())

    def test_valid_verification_code(self):

        """Test whether it redirects to the signup page upon inputting a valid verification code"""

        data = {'code': 'AAAA'}
        response = self.client.post(reverse('verify'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_invalid_verification_code(self):

        """Test that it does not redirect to the signup page upon inputting an invalid verification code"""

        data = {'code': 'AAAAA'}
        response = self.client.post(reverse('verify'), data=data)
        self.assertEqual(response.status_code, 200)

    def test_verification_page(self):

        """Test whether the given url renders the correct verification page"""

        response = self.client.get(reverse('verify'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'verification_page.html')

    def test_dentist_list_page(self):

        """Test whether the dentist instances created are shown in the dentist list."""

        user5 = User.objects.create_user(username='tester', password='a')

        user5.save()

        Staff5 = Staff.objects.create(user=user5, role='dentist')
        Staff5.save()

        user6 = User.objects.create_user(username='checker', password='a')

        user6.save()

        Staff6 = Staff.objects.create(user=user6, role='dentist')
        Staff6.save()



        response = self.client.get(reverse('dentist-view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dentist_view.html')
        self.assertEquals(response.context['dentists'][0], self.dentist)
        self.assertEquals(response.context['dentists'][1], Staff5)
        self.assertEquals(response.context['dentists'][2], Staff6)

    def test_patient_list_page(self):

        """Test whether the patient instances created are shown in the dentist list."""

        user5 = User.objects.create_user(username='test5', password='a')

        user5.save()

        patient5 = Patient.objects.create(user=user5, insurance_number='1221211211')
        patient5.save()

        user6 = User.objects.create_user(username='test6', password='a')

        user6.save()

        patient6 = Patient.objects.create(user=user6, insurance_number='1221211211')
        patient6.save()

        self.client.login(username='test3', password='a')
        response = self.client.get(reverse('patient-list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff_patients.html')
        self.assertEquals(response.context['patient_list_obj'][0], self.patient)
        self.assertEquals(response.context['patient_list_obj'][1], patient5)
        self.assertEquals(response.context['patient_list_obj'][2], patient6)

    def test_specific_patient_page(self):

        """Test if clicking on a patient renders a page of their profile"""

        self.client.login(username='test3', password='a')
        response = self.client.get(reverse('patient-detail', kwargs={'pk': self.patient.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_profile.html')

    def test_specific_dentist_page(self):

        """Test if clicking on a dentist renders a page of their profile"""

        self.client.login(username='test3', password='a')
        response = self.client.get(reverse('dentist-detail', kwargs={'pk': self.dentist.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dentist_profile.html')

    def test_staff_signup_page(self):

        """Test if staff signup is rendered correctly"""

        response = self.client.get(self.staffsignup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff_signup.html')

    def test_receptionist_add_patient_page(self):

        """Test if the add patient form is rendered correctly"""

        self.client.login(username='test3', password='a')
        response = self.client.get(self.addpatient_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_patient.html')

    def test_not_authenticated_add_patient_page(self):

        """Test that an unauthenticated user cannot add a patient"""

        response = self.client.get(self.addpatient_url)
        self.assertEquals(response.status_code, 302)

    def test_not_authenticated_patient_homepage(self):

        """Test that an unauthenticated patient is directed to the homepage"""

        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_authenticated_patient_homepage(self):

        """Test that an authenticated patient is directed to the patient homepage"""

        self.client.login(username='test1', password='a')
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'patient_home.html')

    def test_patient_signup_page(self):

        """Test that the patient signup page is rendered correctly"""

        response = self.client.get(self.patientsignup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_signup.html')
