from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('staff/', views.staff_list, name='staff_list'),
    path('patients/', views.patient_list, name='patient_list'),
    path('rooms/', views.room_list, name='room_list'),
    path('add_room/', views.add_room, name='add_room'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('edit_patient/', views.edit_patient, name='edit_patient'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('get_patient/<int:patient_id>/', views.get_patient, name='get_patient'),
    path('get_room/<int:room_id>/', views.get_room, name='get_room'),
    path('get_staff/<int:staff_id>/', views.get_staff, name='get_staff'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('edit_staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('edit_room/<int:room_id>/', views.edit_room, name='edit_room'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('room_availability/<int:room_id>/', views.room_availability, name='room_availability'),
    path('room_availability/<int:room_id>/', views.room_availability, name='room_availability'),
    path('reservation_details/<int:reservation_id>/', views.reservation_details, name='reservation_details'),
    path('patient/<int:patient_id>/reservations/', views.patient_reservations, name='patient_reservations'),
    path('get_reservation/<int:reservation_id>/', views.get_reservation, name='get_reservation'),
    path('edit_reservation/', views.edit_reservation, name='edit_reservation'),
    path('room_reservations/<int:room_id>/', views.room_reservations, name='room_reservations')


]
