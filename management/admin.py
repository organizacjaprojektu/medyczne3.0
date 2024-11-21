from django.contrib import admin
from .models import Room, Patient, Staff
# Register your models here.
admin.site.register(Room)
admin.site.register(Patient)
admin.site.register(Staff)