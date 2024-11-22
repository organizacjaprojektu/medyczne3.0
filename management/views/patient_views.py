from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from management.helpers.decorators import role_required
from management.models import Patient, Room
from management.helpers.utils import create_patient


@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


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
def assign_patient_to_room(request, patient_id, room_id):
    if request.method == 'POST':
        try:
            patient = Patient.objects.get(id=patient_id)
            room = Room.objects.get(id=room_id)
            if room.get_available_spaces() > 0:
                if patient.assigned_room is None:
                    patient.assigned_room = room
                    patient.save()
                else:
                    return JsonResponse({'success': False, 'error': 'Patient already assigned to room.'})
            else:
                return JsonResponse({'success': False, 'error': 'No available spaces in this room.'})
            return JsonResponse({'success': True, 'message': 'Patient assigned to room successfully.'})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found.'})
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Room not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

class CustomLoginView(LoginView):
    template_name = 'login.html'