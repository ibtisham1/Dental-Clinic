from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [

    path(r'^signup/', views.signup, name="signup"),
    path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    path('staff_home/', views.staff_home, name='staff_home'),
    path('patient_home/', views.patient_home, name='patient_home'),
    path('add_patient/', views.add_patient.as_view(), name='add-patient'),
    path('dentist_view/', views.dentist_view.as_view(), name='dentist-view'),
    path('dentist_view/<int:pk>/', views.dentist_profile_view.as_view(), name='dentist-detail'),
    path('patient_signup/', views.Patient_signup.as_view(), name='patient_signup'),
    path('verification/', views.verification, name='verify'),
    path('staff_signup/', views.Staff_signup.as_view(), name='staff_signup'),
    path('patient/<int:pk>/', views.PatientProfileView.as_view(), name='patient-detail'),
    path('staff/patients/', views.PatientListView.as_view(), name='patient-list'),
    path('username_check/', views.ajax_username_val, name='username-val'),
    path('email_check/', views.ajax_email_val, name='email-val'),
]
