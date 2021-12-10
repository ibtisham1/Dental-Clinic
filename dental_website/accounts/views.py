from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import User, Patient, Staff
from .form import PatientSignUpForm, StaffSignUpForm, Verification
from django.views import generic
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.apps import apps
from django.utils import timezone
from datetime import timedelta
from bookings.models import Booking
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """
    This function renders our homepage.

    """

    if not request.user.is_authenticated:
        return render(request, "homepage.html")

    current_user = User.objects.get(username=request.user.username)

    if Patient.objects.filter(pk=current_user).exists():
        return render(request, "patient_home.html")
    elif Staff.objects.filter(pk=current_user).exists():
        staff_object = Staff.objects.get(pk=current_user)
        return staff_home(request, staff_object, current_user)
    else:

        return render(request, "homepage.html")

def signup(request):
    """
       This function renders our signup homepage.

       """
    return render(request, "signup.html")


"""Simple is Better Than Complex. (2016). How to Work With AJAX Request With Django. 
[online] Available at: https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html."""

""" *************************************************************************************
*	Title: How to  worth with AJAX Request with Django
*	Author: Vitor Freitas
*	Date: 19th November, 2020
*	Code version: None
*	Availability: https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html
*
********************************************************************************* """


# Create your views here.
def ajax_username_val(request):
    username = request.GET.get('username', None)
    username_Info = {
        'existing': User.objects.filter(username=username).exists()
    }
    return JsonResponse(username_Info)


def ajax_email_val(request):
    email = request.GET.get('email', None)
    email_Info = {
        'existing': User.objects.filter(email=email).exists()
    }
    return JsonResponse(email_Info)

"""Staff_Home
    Renders the home page for a staff member.
    Context object includes staff role to be able to differentiate between
    different types of staff members
"""

def staff_home(request, staff, user):
    if not request.user.is_authenticated:
        return render(request, "homepage.html")

    booking_object = apps.get_model('bookings', 'Booking')
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=1)
    count = Booking.objects.filter(approved=False).count()
    if staff.role == "dentist":
        bookings = booking_object.objects.filter(doctor=Staff.objects.get(pk=user), date__range=(start_date, end_date),
                                                 approved=True)
    elif staff.role == "assistant":
        bookings = booking_object.objects.filter(assistant=Staff.objects.get(pk=user),
                                                 date__range=(start_date, end_date), approved=True)
    else:
        bookings = booking_object.objects.filter(date__range=(start_date, end_date), approved=True)

    context = {
        'role': staff.role,
        'firstname': user.first_name,
        'lastname': user.last_name,
        'booking_list': bookings.order_by('date'),
        'num_bookings': bookings.count(),
        'unapproved_count': count,
    }

    return render(request, "staff_home.html", context)


"""patient_home
    Renders the home page for a patient.
"""

def patient_home(request):

    return render(request, "patient_home.html")

"""Patient_signup
    This view renders the signup form for a patient
    Logs them in after successful form completion
"""
class Patient_signup(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'patient_signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


"""add_patient
    This view renders the signup form for a patient
    on the staff side. A receptionist is also allowed to create
    a patient.
"""

class add_patient(LoginRequiredMixin,CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'add_patient.html'

    def form_valid(self, form):
        form.save()
        user = self.request.user
        staff = Staff.objects.get(user=user)
        return staff_home(self.request, staff, user)

"""Staff_signup
    This view renders the signup form for a staff member
    Upon successful logging in they are directed to their homepage.
"""

class Staff_signup(CreateView):
    model = User
    form_class = StaffSignUpForm
    template_name = 'staff_signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

"""verification
    This view renders the verification form for a staff member
    Upon successful input of the staff code they are directed
    to the staff signup form.
"""

def verification(request):
    if request.method == 'POST':
        form = Verification(request.POST)  # if post method then form will be validated
        if form.is_valid():
            cd = form.cleaned_data
            code = cd.get('code')

            if code != 'AAAA':
                messages.error(request, 'Code incorrect')
                pass
            else:
                return redirect('staff_signup')

    else:
        form = Verification()  # blank form object just to pass context if not post method
    return render(request, "verification_page.html", {'form': form})


"""PatientProfileView
    This view renders the details of a particular patient
"""

class PatientProfileView(generic.DetailView):
    model = Patient
    template_name = 'patient_profile.html'

    def get_context_data(self, **kwargs):
        context = super(PatientProfileView, self).get_context_data(**kwargs)
        role = getRole(self.request)
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name

        return context

"""Dentist_Profile_View
    This view renders the details of a particular Dentist
"""
class dentist_profile_view(generic.DetailView):
    model = Staff
    template_name = 'dentist_profile.html'
    context_object_name = 'dentist'

    def get_context_data(self, **kwargs):
        context = super(dentist_profile_view, self).get_context_data(**kwargs)

        return context

"""PatientListView
   As a staff member, this view renders a list of all patients.
   The patient name can be clicked to discover further information about the patient
"""
class PatientListView(generic.ListView):
    """View all Patients as a Staff.."""
    model = Patient
    template_name = 'staff_patients.html'
    context_object_name = 'patient_list_obj'  # name for the list as a template variable
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        role = getRole(self.request)
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name

        return context

"""Dentist_View
    This view renders a list of all available dentists from the clinic.
"""
class dentist_view(generic.ListView):
    model = Staff
    template_name = 'dentist_view.html'

    def get_context_data(self, **kwargs):
        context = super(dentist_view, self).get_context_data(**kwargs)
        context['dentists'] = Staff.objects.filter(role='dentist')
        return context


def getRole(request):

    current_user = User.objects.get(username=request.user.username)
    if Staff.objects.filter(pk=current_user).exists():
        staff_object = Staff.objects.get(pk=current_user)
        return staff_object.role
    return None