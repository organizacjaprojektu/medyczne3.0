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
]
