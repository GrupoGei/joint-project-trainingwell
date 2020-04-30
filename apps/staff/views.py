from django.shortcuts import render, redirect
from apps.reservations.models import *


def dashboard_installations(request):
    installations = Installation.objects.all()

    context = {
        'installations': installations
    }

    return render(request, 'installation_list_staff.html', context)


def dashboard_reserves(request):
    reserves = Reservation.objects.all()

    context = {
        'reserves': reserves
    }

    return render(request, 'reserves_list_staff.html', context)


def dashboard_cancel_reserve(request, pk_reserve):
    reserve_selected = Reservation.objects.get(pk=pk_reserve)
    reserve_selected.delete()

    return redirect('/dashboard/reserves')
