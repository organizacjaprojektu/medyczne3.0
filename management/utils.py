from django.contrib.auth.models import User
from .models import Staff, Patient, Room


def create_account(password, first_name, last_name, position, role='USER', email=None):
    """
    Create a new staff member in the database.

    """
    user = User.objects.create_user(first_name+'_'+last_name, email, password)

    staff = Staff.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        position=position,
        role=role
    )

    return user, staff

def create_patient(first_name, last_name, dob):
    """
    Create a new patient in the database.
    """
    patient = Patient.objects.create(
        first_name=first_name,
        last_name=last_name,
        birth_date=dob
    )
    return patient


def create_room(room_number, room_type, description, capacity):
    """
    Create a new room in the database.
    """
    room = Room.objects.create(
        room_number=room_number,
        type=room_type,
        description=description,
        capacity=capacity
    )
    return room
