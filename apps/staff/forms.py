from django import forms
from apps.reservations.models import Installation, Sport


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


class PriceForm(forms.ModelForm):
    class Meta:
        model = Installation
        fields = (
            'price_base',
            'discount'
        )
        labels = {
            'price_base': "Preu per hora",
            'discount': "Descompte",
        }


class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = (
            'name',
        )
        labels = {
            'name': "Nom de l'esport",
        }
