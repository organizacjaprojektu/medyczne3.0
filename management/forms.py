from django import forms
from .models import Patient, Room

class AssignRoomForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['assigned_room']  # Pole, które pozwoli wybrać pokój dla pacjenta

    # Opcjonalnie: Możemy dodać dodatkowe ustawienia dla pola assigned_room
    assigned_room = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label="Wybierz pokój")
