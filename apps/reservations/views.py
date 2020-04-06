from django.shortcuts import render
from .models import Installation
from .models import CurrentReservations


# Create your views here.

def show_installations(request):
    installations = Installation.objects.order_by('sports')
    context = {
        'installations': installations,
    }

    return render(request, 'installation_list.html', context)


def show_installations_reserved(request):
    installations_reserved = CurrentReservations.objects.order_by('sports')
    context = {
        'installations_reserved': installations_reserved,
    }

    return render(request, 'installation_reserved_list.html', context)
