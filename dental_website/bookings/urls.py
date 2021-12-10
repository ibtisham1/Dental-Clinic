from django.urls import include, path
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'bookingapi', views.BookingList)

app_name = 'bookings'
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('bookingform/', views.createBooking.as_view(), name='Booking-View'),
    path('<int:pk>/makeBooking/', views.Makebooking.as_view(), name='create_booking'),
    path('<int:pk>/assign/', views.assign, name='assign'),
    path('<int:pk>/patient/', views.patientBookingDetailView.as_view(), name='patient-booking-detail'),
    path('<int:pk>/staff/', views.staffBookingDetailView.as_view(), name='staff-booking-detail'),
    path('staff/mybookings/', views.BookingsByStaff.as_view(), name='staff-booking'),
    path('patient/mybookings/', views.PatientBookings.as_view(), name='patient-booking'),
    path('bookingform/confirmation/',views.bookingConfirmation , name='confirmation'),
    path('bookingform/failure/', views.failedBooking, name='failed'),
    path('staff/allbookings/', views.ReceptionistBookings.as_view(), name='receptionist-list'),
    path('patient/medicalhistory/<int:pk>/', views.MedicalHistory.as_view(), name='patient-medical'),
    path('patient/upcomingbookings/<int:pk>/', views.UpcomingBookings.as_view(), name='patient-upcoming'),
    path('<int:pk>/patient/editbookingform/', views.update_view, name='Edit-Booking-View'),
    path('<int:pk>/patient/cancelbooking/', views.cancel, name='Cancel-Booking'),
    path('<int:pk>/patient/approvebooking/', views.approve, name='Approve-Booking'),
]