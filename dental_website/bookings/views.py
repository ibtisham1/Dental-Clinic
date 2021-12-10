from django.shortcuts import render, redirect
from .models import Booking
from .form import PatientBooking, Assign
from django.views import generic
from django.views.generic import CreateView
from accounts.models import User, Patient, Staff
from django.apps import apps
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from rest_framework import viewsets
from .serializers import BookingSer
from accounts import views

"""Garner, B. (2020). Build your first REST API with Django REST Framework. [online] Medium. 
Available at: https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c."""
"""Title: Build a REST API in 30 minutes with Django REST Framework

*	Author: Bennet Garner
*	Date: 19th November, 2020
*	Code version: None
*	Availability: https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c
*
****************************************************************************
"""


class BookingList(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Booking.objects.all().order_by('id')
    serializer_class = BookingSer


"""showBooking 
    Shows all booking"""


def showBooking(request):
    queryset = Booking.objects.all()
    context = {
        "booking_list": queryset
    }
    return render(request, "ShowBooking.html", context)


"""bookingConfirmation 
    renders a view which shows a confirmation message when creating a booking"""


def bookingConfirmation(request):
    return render(request, "booking_confirmation.html")


"""failedBooking 
    Renders a view which shows a failed message when creating a booking"""


def failedBooking(request):
    return render(request, "booking_failed.html")


"""patientBookingDetailView 
    Renders a view which shows a detailed information on a booking in the patient perspective"""


class patientBookingDetailView(generic.DetailView):
    model = Booking
    template_name = 'bookings/patient_bookings_detail.html'


"""staffBookingDetailView 
    Renders a view which shows a detailed information on a booking in the staff perspective"""


class staffBookingDetailView(generic.DetailView):
    model = Booking
    template_name = 'bookings/staff_booking_detail.html'

    def get_context_data(self, **kwargs):
        context = super(staffBookingDetailView, self).get_context_data(**kwargs)
        role = views.getRole(self.request)
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name

        return context


"""Generic class-based view listing bookings associated with current user."""


class BookingsByStaff(generic.ListView):
    model = Booking
    template_name = 'bookings/staff_bookings.html'
    paginate_by = 5

    def get_queryset(self):
        role = views.getRole(self.request)
        #Retrieve the correct bookings for the associated user and his/her role
        if role == "dentist":
            bookings = Booking.objects.filter(doctor=Staff.objects.get(pk=self.request.user),
                                              approved=True).order_by('date')
        else:
            bookings = Booking.objects.filter(assistant=Staff.objects.get(pk=self.request.user),
                                              approved=True).order_by('date')
        return bookings

    def get_context_data(self, **kwargs):
        context = super(BookingsByStaff, self).get_context_data(**kwargs)
        role = views.getRole(self.request)
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name

        #Retrieve the correct bookings for the associated user and his/her role

        if role == "dentist":
            context['previous'] = Booking.objects.filter(doctor=Staff.objects.get(pk=self.request.user),
                                                         date__lte=timezone.now(), approved=True).order_by('date')
            context['upcoming'] = Booking.objects.filter(doctor=Staff.objects.get(pk=self.request.user),
                                                         date__gte=timezone.now(), approved=True).order_by('date')
        else:
            context['previous'] = Booking.objects.filter(assistant=Staff.objects.get(pk=self.request.user),
                                                         date__lte=timezone.now(), approved=True).order_by('date')
            context['upcoming'] = Booking.objects.filter(assistant=Staff.objects.get(pk=self.request.user),
                                                         date__gte=timezone.now(), approved=True).order_by('date')

        return context


"""Generic class-based view listing bookings associated with current patient user."""
class PatientBookings(generic.ListView):


    model = Booking
    template_name = 'bookings/patient_bookings.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PatientBookings, self).get_context_data(**kwargs)
        context['bookings'] = Booking.objects.filter(patient=self.request.user, approved=True)
        context['unapproved'] = Booking.objects.filter(patient=self.request.user, approved=False)
        return context


"""Renders the booking form for creating a booking"""
class createBooking(CreateView):
    model = Booking
    form_class = PatientBooking
    template_name = 'BookingView.html'

    def form_valid(self, form):
        try:
            booking = form.save()
            booking.patient = User.objects.get(username=self.request.user.username)
            count = Booking.objects.all().count()
            booking.id = count + 1
            booking.save()
            return redirect('bookings:confirmation')
        except:
            return redirect('bookings:failed')

"""Renders the booking form for creating a booking in the perspective of a receptionist"""

class Makebooking(CreateView):
    model = Booking
    form_class = PatientBooking
    template_name = 'staff_booking.html'

    def form_valid(self, form):
        booking = form.save()
        booking.patient = User.objects.get(pk=self.kwargs.get('pk'))
        count = Booking.objects.all().count()
        booking.id = count + 1
        booking.approved = True
        booking.save()
        return redirect('bookings:receptionist-list')

    def get_context_data(self, **kwargs):
        context = super(Makebooking, self).get_context_data(**kwargs)
        context['patient'] = User.objects.get(pk=self.kwargs['pk'])
        return context

"""Cancels a booking """

def cancel(request, pk):
    Booking.objects.get(pk=pk).delete()

    try:
        Staff.objects.get(user=request.user)
        staff = Staff.objects.get(user=request.user)
        if staff.role == "receptionist":
            return redirect('bookings:receptionist-list')
        else:
            return redirect('bookings:staff-booking')
    except:
        return redirect('bookings:patient-booking')


"""Gives receptionist ability to approve a booking"""
def approve(request, pk):
    booking = Booking.objects.get(pk=pk)
    booking.approved = True
    booking.save()

    return redirect('bookings:receptionist-list')


"""Allows the editing of a booking, renders the form previously filled in for the booking"""
def update_view(request, pk):
    context = {}

    booking = Booking.objects.get(pk=pk)

    form = PatientBooking(request.POST or None, instance=booking)

    if form.is_valid():
        try:
            form.save()
            booking.save()
            return redirect('bookings:receptionist-list')
        except:
            return HttpResponseRedirect(request.path_info)

    context["form"] = form

    return render(request, "EditBookingView.html", context)


"""View all Bookings as a Receptionist."""
class ReceptionistBookings(generic.ListView):

    model = Booking
    template_name = 'bookings/receptionist_bookings.html'
    context_object_name = 'booking_list_obj'  # name for the list as a template variable

    def get_context_data(self, **kwargs):
        context = super(ReceptionistBookings, self).get_context_data(**kwargs)
        role = views.getRole(self.request)
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name
        context['previous'] = Booking.objects.filter(date__lte=timezone.now(), approved=True).order_by('-date')
        context['upcoming'] = Booking.objects.filter(date__gte=timezone.now(), approved=True).order_by('-date')
        context['unapproved'] = Booking.objects.filter(date__gte=timezone.now(), approved=False).order_by('-date')
        return context

"""Generic class-based view listing PREVIOUS bookings associated with viewed Patient."""
class MedicalHistory(generic.ListView):
    model = Booking
    template_name = 'bookings/medical_history.html'
    context_object_name = 'booking_list'
    paginate_by = 5

    def get_queryset(self):
        patient_user = self.kwargs['pk']
        return Booking.objects.filter(patient=patient_user, date__lte=timezone.now(), approved=True).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(MedicalHistory, self).get_context_data(**kwargs)
        role = views.getRole(self.request)
        user_model = apps.get_model('accounts', 'User')
        current_user = user_model.objects.get(pk=self.kwargs['pk'])
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name
        context['patient_first'] = current_user.first_name
        context['patient_last'] = current_user.last_name

        return context

"""Generic class-based view listing UPCOMING bookings associated with viewed Patient."""
class UpcomingBookings(generic.ListView):
    model = Booking
    template_name = 'bookings/upcoming_bookings.html'
    context_object_name = 'booking_list'
    paginate_by = 5

    def get_queryset(self):
        patient_user = self.kwargs['pk']
        return Booking.objects.filter(patient=patient_user, date__gte=timezone.now(), approved=True).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(UpcomingBookings, self).get_context_data(**kwargs)
        role = views.getRole(self.request)
        user_model = apps.get_model('accounts', 'User')
        current_user = user_model.objects.get(pk=self.kwargs['pk'])
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name
        context['patient_first'] = current_user.first_name
        context['patient_last'] = current_user.last_name

        return context

"""Renders the assignment form whereby a receptionist can pick an assistant to assign to a booking"""
def assign(request, pk):
    context = {}
    if request.method == 'POST':
        form = Assign(request.POST)  # if post method then form will be validated
        if form.is_valid():
            cd = form.cleaned_data
            assistant = cd.get('assistant')

            booking = Booking.objects.get(id=pk)
            booking.assistant = assistant
            booking.save()
            return redirect('bookings:receptionist-list')
    else:
        form = Assign()

    context['form'] = form
    context['booking'] = Booking.objects.get(id=pk)
    return render(request, "assign.html", context)
