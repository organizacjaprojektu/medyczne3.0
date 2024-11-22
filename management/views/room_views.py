from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from management.helpers.decorators import role_required
from management.models import Room
from management.helpers.utils import create_room

@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

@login_required()
def get_all_rooms(request):
    rooms = Room.objects.all()
    rooms_data = []

    for room in rooms:
        rooms_data.append({
            'id': room.id,
            'room_number': room.room_number,
            'type': room.type,
            'description': room.description,
            'capacity': room.capacity,
            'available_spaces': room.get_available_spaces()
        })

    return JsonResponse({'rooms': rooms_data})



@login_required
@role_required('ADMIN')
def add_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('type')
        capacity = request.POST.get('capacity')
        description = request.POST.get('description')

        if not room_number or not room_type:
            return render(request, 'room_list.html', {
                'error': 'Fields required: Room number, Type',
                'rooms': Room.objects.all()
            })

        if room_type == 'PATIENT' and not capacity:
            return render(request, 'room_list.html', {
                'error': 'Capacity is required for Patient rooms.',
                'rooms': Room.objects.all()
            })
        if room_type != 'PATIENT' and not capacity:
            capacity = None

        create_room(room_number, room_type, capacity, description)

        return render(request, 'room_list.html', {
            'success': 'Room added successfully.',
            'rooms': Room.objects.all()
        })

    return render(request, 'room_list.html', {'rooms': Room.objects.all()})



@login_required
@role_required('ADMIN')
def edit_room(request, room_id):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('type')
        description = request.POST.get('description')
        capacity = request.POST.get('capacity')  # Pobierz capacity z formularza

        try:
            room = Room.objects.get(id=room_id)
            room.room_number = room_number
            room.type = room_type
            room.description = description

            if room_type == 'PATIENT':
                room.capacity = capacity  # Zapisz capacity tylko dla pokojów typu Patient
            else:
                room.capacity = None  # Usuń wartość capacity dla innych typów

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
        'capacity': room.capacity,
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
