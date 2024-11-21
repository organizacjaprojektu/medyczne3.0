from django.contrib.auth.views import LoginView
from django.http import JsonResponse
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
@login_required
@role_required('ADMIN')
def edit_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')

        try:
            patient = Patient.objects.get(id=patient_id)
            patient.first_name = first_name
            patient.last_name = last_name
            patient.birth_date = dob
            patient.save()

            return JsonResponse({'success': True, 'message': 'Patient updated successfully.'})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request.'})


@login_required
@role_required('ADMIN')
def get_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    data = {
        'id': patient.id,
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'birth_date': patient.birth_date.isoformat(),
    }
    return JsonResponse(data)


@login_required
@role_required('ADMIN')
def delete_patient(request, patient_id):
    if request.method == 'DELETE':
        try:
            patient = Patient.objects.get(id=patient_id)
            patient.delete()
            return JsonResponse({'success': True, 'message': 'Patient deleted successfully.'})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
@role_required('ADMIN')
def edit_staff(request, staff_id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        position = request.POST.get('position')
        role = request.POST.get('role')

        try:
            staff = Staff.objects.get(id=staff_id)
            staff.first_name = first_name
            staff.last_name = last_name
            staff.position = position
            staff.role = role
            staff.save()

            return JsonResponse({'success': True, 'message': 'Staff updated successfully.'})
        except Staff.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Staff not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@login_required
@role_required('ADMIN')
def delete_staff(request, staff_id):
    if request.method == 'DELETE':
        try:
            staff = Staff.objects.get(id=staff_id)
            staff.delete()
            return JsonResponse({'success': True, 'message': 'Staff deleted successfully.'})
        except Staff.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Staff not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
@role_required('ADMIN')
def get_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    data = {
        'id': staff.id,
        'first_name': staff.first_name,
        'last_name': staff.last_name,
        'position': staff.position,
        'role': staff.role,
    }
    return JsonResponse(data)


@login_required
@role_required('ADMIN')
def edit_room(request, room_id):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('type')
        description = request.POST.get('description')

        try:
            room = Room.objects.get(id=room_id)
            room.room_number = room_number
            room.type = room_type
            room.description = description
            room.save()

            return JsonResponse({'success': True, 'message': 'Room updated successfully.'})
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Room not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request.'})


@login_required
@role_required('ADMIN')
def get_room(request, room_id):
    room = Room.objects.get(id=room_id)
    data = {
        'id': room.id,
        'room_number': room.room_number,
        'type': room.type,
        'description': room.description,
    }
    return JsonResponse(data)


@login_required
@role_required('ADMIN')
def delete_room(request, room_id):
    if request.method == 'DELETE':
        try:
            room = Room.objects.get(id=room_id)
            room.delete()
            return JsonResponse({'success': True, 'message': 'Room deleted successfully.'})
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Room not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@login_required
def home(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'