from django.shortcuts import render
from django.db.models import Q  # new

# Create your views here.
from django.views.generic import ListView
from bookings import models
from accounts import views
from django.apps import apps

""" """
class SearchReceptionist(ListView):
    model = models.Booking
    template_name = 'search_receptionist.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = models.Booking.objects.filter(
            Q(title__icontains=query) | Q(doctor__user__first_name__icontains=query)
            | Q(doctor__user__last_name__icontains=query) | Q(patient__first_name__icontains=query)
            | Q(patient__last_name__icontains=query) | Q(assistant__user__first_name__icontains=query)
            | Q(assistant__user__last_name__icontains=query)
        )
        return object_list.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(SearchReceptionist, self).get_context_data(**kwargs)
        role = views.getRole(self.request)
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name
        context['query'] = self.request.GET.get('q')
        return context

""""""
class SearchStaff(ListView):
    model = models.Booking
    template_name = 'search_staff.html'
    context_object_name = 'search_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = models.Booking.objects.filter(
            Q(title__icontains=query) | Q(doctor__user__first_name__icontains=query)
            | Q(doctor__user__last_name__icontains=query) | Q(patient__first_name__icontains=query)
            | Q(patient__last_name__icontains=query) | Q(assistant__user__first_name__icontains=query)
            | Q(assistant__user__last_name__icontains=query)
        )

        role = views.getRole(self.request)
        staff_model = apps.get_model('accounts', 'Staff')
        if role == 'dentist':
            final_list = object_list.filter(doctor=staff_model.objects.get(pk=self.request.user))
        elif role == 'assistant':
            final_list = object_list.filter(assistant=staff_model.objects.get(pk=self.request.user))
        else:
            final_list = object_list

        return final_list.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(SearchStaff, self).get_context_data(**kwargs)
        role = views.getRole(self.request)
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name
        context['query'] = self.request.GET.get('q')
        return context


class SearchPatient(ListView):
    model = models.Booking
    template_name = 'search_patient.html'
    context_object_name = 'search_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = models.Booking.objects.filter(
            Q(title__icontains=query) | Q(doctor__user__first_name__icontains=query)
            | Q(doctor__user__last_name__icontains=query) | Q(patient__first_name__icontains=query)
            | Q(patient__last_name__icontains=query) | Q(assistant__user__first_name__icontains=query)
            | Q(assistant__user__last_name__icontains=query)
        )
        final_list = object_list.filter(patient=self.request.user)
        return final_list.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(SearchPatient, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class SearchPeople(ListView):
    model = models.User
    template_name = 'search_staff_patient.html'
    context_object_name = 'search_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = models.User.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
        return object_list.order_by('-last_name','-first_name')

    def get_context_data(self, **kwargs):
        context = super(SearchPeople, self).get_context_data(**kwargs)
        role = views.getRole(self.request)
        context['role'] = role
        context['firstname'] = self.request.user.first_name
        context['lastname'] = self.request.user.last_name
        context['query'] = self.request.GET.get('q')
        return context
