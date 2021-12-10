from django.urls import path

from . import views

urlpatterns = [
    path('receptionist/search/', views.SearchReceptionist.as_view(), name='search_receptionist'),
    path('staff/search/', views.SearchStaff.as_view(), name='search_staff'),
    path('patient/search/', views.SearchPatient.as_view(), name='search_patient'),
    path('staff/patient/search/', views.SearchPeople.as_view(), name='search_people'),

]