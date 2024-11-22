from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from management.helpers.decorators import role_required
from management.models import Staff
from management.helpers.utils import create_account


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff_members': staff_members})

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

