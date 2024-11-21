from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .decorators import role_required
from .models import Patient, Room, Staff
from .utils import create_account, create_room, create_patient


@login_required
def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff_members': staff_members})

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


@login_required
@role_required('ADMIN')
def add_staff(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        position = request.POST.get('position')
        role = request.POST.get('role', 'USER')  # Default role is 'USER'

        if not password or not first_name or not last_name or not position:
            return render(request, 'staff_list.html', {
                'error': 'All fields are required.',
                'staff_members': Staff.objects.all()
            })

        create_account(password, first_name, last_name, position, role=role)

        return render(request, 'staff_list.html', {
            'success': 'Account created successfully.',
            'staff_members': Staff.objects.all()
        })

    return render(request, 'staff_list.html', {'staff_members': Staff.objects.all()})

@login_required
@role_required('ADMIN')
def add_patient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')

        if not first_name or not last_name or not dob:
            return render(request, 'patient_list.html', {
                'error': 'All fields are required.',
                'patients': Patient.objects.all()
            })

        create_patient(first_name, last_name, dob)

        return render(request, 'patient_list.html', {
            'success': 'Patient added successfully.',
            'patients': Patient.objects.all()
        })

    return render(request, 'patient_list.html', {'patients': Patient.objects.all()})


@login_required
@role_required('ADMIN')
def add_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('type')
        description = request.POST.get('description')

        if not room_number or not room_type:
            return render(request, 'room_list.html', {
                'error': 'Fields required: Room number, Type',
                'rooms': Room.objects.all()
            })

        create_room(room_number, room_type, description)

        return render(request, 'room_list.html', {
            'success': 'Room added successfully.',
            'rooms': Room.objects.all()
        })

    return render(request, 'room_list.html', {'rooms': Room.objects.all()})
@login_required
def home(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'