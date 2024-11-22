from django.urls import path
from django.contrib.auth.views import LogoutView
from .views.patient_views import CustomLoginView
from .views import patient_views
from .views import room_views
from .views import staff_views
staff_patterns = [
    path('', staff_views.home, name='home'),
    path('home/', staff_views.home, name='home'),
    path('staff/', staff_views.staff_list, name='staff_list'),
    path('delete_staff/<int:staff_id>/', staff_views.delete_staff, name='delete_staff'),
    path('edit_staff/<int:staff_id>/', staff_views.edit_staff, name='edit_staff'),
    path('add_staff/', staff_views.add_staff, name='add_staff'),
    path('get_staff/<int:staff_id>/', staff_views.get_staff, name='get_staff'),
]
patient_patterns = [
    path('patients/', patient_views.patient_list, name='patient_list'),
    path('add_patient/', patient_views.add_patient, name='add_patient'),
    path('edit_patient/', patient_views.edit_patient, name='edit_patient'),
    path('delete_patient/<int:patient_id>/', patient_views.delete_patient, name='delete_patient'),
    path('get_patient/<int:patient_id>/', patient_views.get_patient, name='get_patient'),
    path('assign_patient/<int:patient_id>/to-room/<int:room_id>/', patient_views.assign_patient_to_room, name='assign_patient_to_room'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
room_patterns = [
    path('get_all_rooms/', room_views.get_all_rooms, name='get_all_rooms'),
    path('get_room/<int:room_id>/', room_views.get_room, name='get_room'),
    path('rooms/', room_views.room_list, name='room_list'),
    path('add_room/', room_views.add_room, name='add_room'),
    path('delete_room/<int:room_id>/', room_views.delete_room, name='delete_room'),
    path('edit_room/<int:room_id>/', room_views.edit_room, name='edit_room'),
]
urlpatterns = []
urlpatterns.extend(staff_patterns)
urlpatterns.extend(room_patterns)
urlpatterns.extend(patient_patterns)
