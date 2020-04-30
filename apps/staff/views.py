from django.shortcuts import render
from apps.reservations.models import *


def dashboard(request):
    installations = Installation.objects.all()

    context = {
        'installations': installations
    }

    return render(request, 'installation_list_responsible.html', context)
