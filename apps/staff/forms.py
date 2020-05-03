from django import forms
from apps.reservations.models import Installation


class InstallationForm(forms.ModelForm):
    class Meta:
        model = Installation
        fields = (
            "name",
            "description",
            "image",
            "capacity",
            "sports",
        )
        labels = {
            "name": "Nom de la instal·lació",
            "description": "Descripció",
            "image": "Imatge",
            "capacity": "Capacitat",
            "sports": "Esports"
        }