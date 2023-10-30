from .models import CustomUser  # Asegúrate de que la ruta de importación sea correcta
from django import forms


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'rol')
