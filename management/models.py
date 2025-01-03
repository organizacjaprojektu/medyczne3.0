from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    ROOM_TYPES = [
        ('OPERATING', 'Operating room'),
        ('CONSULTATION', 'Consultation room'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    description = models.TextField(blank=True, null=True)
    room_number = models.BigIntegerField()
    capacity = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.name} ({self.type})"


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    registration_date = models.DateTimeField(auto_now_add=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Staff(models.Model):
    ROLES = [
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    role = models.CharField(max_length=5, choices=ROLES, default='USER')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"


class Reservation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reservation for {self.patient} in {self.room} ({self.start_date} to {self.end_date})"
