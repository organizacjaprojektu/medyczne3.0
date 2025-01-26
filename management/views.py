from django.contrib.auth.views import LoginView
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from .decorators import role_required
from .models import Patient, Room, Staff, Reservation
from .utils import create_account, create_room, create_patient


@login_required
def reservation_details(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)

        data = {
            'patient': {
                'first_name': reservation.patient.first_name,
                'last_name': reservation.patient.last_name
            },
            'room': {
                'name': reservation.room.name,
                'room_number': reservation.room.room_number
            },
            'start_date': reservation.start_date.strftime('%Y-%m-%d'),
            'end_date': reservation.end_date.strftime('%Y-%m-%d'),
            'description': reservation.description or 'No description provided',  # Handle missing description
        }
        return JsonResponse(data)

    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Reservation not found'}, status=404)


def room_availability(request, room_id):
    month = int(request.GET.get('month', datetime.now().month))
    year = int(request.GET.get('year', datetime.now().year))

    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)

    start_date = datetime(year, month, 1).date()
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    dates = [start_date + timedelta(days=i) for i in range(-1, (end_date - start_date).days + 1)]

    reservations = Reservation.objects.filter(
        room=room,
        start_date__lte=end_date,
        end_date__gte=start_date
    )

    availability = {}
    for date in dates:
        date_str = date.strftime('%Y-%m-%d')
        booked_beds = reservations.filter(start_date__lte=date, end_date__gte=date).count()
        availability[date_str] = room.capacity - booked_beds

    return JsonResponse(availability, safe=False)


@login_required
def reservation_list(request):
    error = request.session.pop('form_error', None)
    success = request.session.pop('form_success', None)
    return render(request, 'reservation_list.html', {
        'reservations': Reservation.objects.all(),
        'patients': Patient.objects.all(),
        'rooms': Room.objects.all(),
        'error': error,
        'success': success,
    })

@login_required
def patient_reservations(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        reservations = Reservation.objects.filter(patient=patient).order_by('-start_date')
        return render(request, 'patient_reservations.html', {
            'patient': patient,
            'reservations': reservations,
        })
    except Patient.DoesNotExist:
        raise Http404("Patient not found")


from django.shortcuts import redirect
from django.urls import reverse

@login_required
def add_reservation(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        room_id = request.POST.get('room_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        if not patient_id or not room_id or not start_date or not end_date:
            request.session['form_error'] = 'All fields are required.'
            return redirect(reverse('reservation_list'))

        existing_reservations = Reservation.objects.filter(
            room_id=room_id,
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        if existing_reservations.count() >= Room.objects.get(id=room_id).room_number:
            request.session['form_error'] = 'Room is fully booked for the selected dates.'
            return redirect(reverse('reservation_list'))

        patient = Patient.objects.get(id=patient_id)
        room = Room.objects.get(id=room_id)
        Reservation.objects.create(
            patient=patient,
            room=room,
            start_date=start_date,
            end_date=end_date,
            description=description
        )

        request.session['form_success'] = 'Reservation created successfully.'
        return redirect(reverse('reservation_list'))

    # If not a POST request, just redirect to the reservation list
    return redirect(reverse('reservation_list'))



@login_required
@role_required('ADMIN')
def delete_reservation(request, reservation_id):
    if request.method == 'DELETE':
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.delete()
            return JsonResponse({'success': True, 'message': 'Reservation deleted successfully.'})
        except Reservation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Reservation not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})




@login_required
def staff_list(request):
    error = request.session.pop('form_error', None)
    success = request.session.pop('form_success', None)
    staff_members = Staff.objects.all()
    return render(request, 'staff_list.html', {
        'staff_members': staff_members,
        'error': error,
        'success': success
    })

@login_required
def patient_list(request):
    error = request.session.pop('form_error', None)
    success = request.session.pop('form_success', None)
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {
        'patients': patients,
        'error': error,
        'success': success
    })


@login_required
def room_list(request):
    error = request.session.pop('form_error', None)
    success = request.session.pop('form_success', None)
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {
        'rooms': rooms,
        'error': error,
        'success': success
    })



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
            request.session['form_error'] = 'All fields are required.'
            return redirect('staff_list')

        create_account(password, first_name, last_name, position, role=role)

        request.session['form_success'] = 'Account created successfully.'
        return redirect('staff_list')

    return redirect('staff_list')

@login_required
@role_required('ADMIN')
def add_patient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')

        if not first_name or not last_name or not dob:
            request.session['form_error'] = 'All fields are required.'
            return redirect('patient_list')

        create_patient(first_name, last_name, dob)

        request.session['form_success'] = 'Patient added successfully.'
        return redirect('patient_list')

    return redirect('patient_list')


@login_required
@role_required('ADMIN')
def add_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('type')
        description = request.POST.get('description')
        capacity = request.POST.get('capacity')

        if not room_number or not room_type:
            request.session['form_error'] = 'Fields required: Room number, Type'
            return redirect('room_list')

        create_room(room_number, room_type, description, capacity)

        request.session['form_success'] = 'Room added successfully.'
        return redirect('room_list')

    return redirect('room_list')


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
def get_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.select_related('patient', 'room').get(id=reservation_id)
        data = {
            'id': reservation.id,
            'patient_id': reservation.patient.id,
            'room_id': reservation.room.id,
            'start_date': reservation.start_date.isoformat(),
            'end_date': reservation.end_date.isoformat(),
            'description': reservation.description or '',
        }
        return JsonResponse(data)
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Reservation not found'}, status=404)

@login_required
@role_required('ADMIN')
def edit_reservation(request):
    if request.method == 'POST':
        try:
            reservation_id = request.POST.get('reservation_id')
            patient_id = request.POST.get('patient_id')
            room_id = request.POST.get('room_id')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            description = request.POST.get('description')

            if not all([reservation_id, patient_id, room_id, start_date, end_date]):
                return JsonResponse({'success': False, 'error': 'All fields are required.'})

            reservation = Reservation.objects.get(id=reservation_id)
            reservation.patient_id = patient_id
            reservation.room_id = room_id
            reservation.start_date = start_date
            reservation.end_date = end_date
            reservation.description = description
            reservation.save()

            return JsonResponse({'success': True, 'message': 'Reservation updated successfully.'})
        except Reservation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Reservation not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def room_reservations(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    reservations = Reservation.objects.filter(room=room).order_by('-start_date')
    return render(request, 'room_reservations.html', {
        'room': room,
        'reservations': reservations,
    })

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