from django.shortcuts import render, redirect
from apps.reservations.models import *
from apps.staff.forms import InstallationForm


def dashboard_installations(request):
    installations = Installation.objects.all()
    sports = Sport.objects.all()

    context = {
        'installations': installations,
        'sports': sports
    }

    return render(request, 'installation_list_staff.html', context)


def dashboard_filtered_installations(request, sport):
    installations = Installation.objects.filter(sports__name=sport)
    sports = Sport.objects.all()
    context = {
        'installations': installations,
        'sports': sports
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


def dashboard_create_installation(request):
    if request.method == 'POST':
        installation_form = InstallationForm(request.POST, request.FILES)
        if installation_form.is_valid():
            installation_form.save()
            return redirect('/dashboard/installations')
    else:
        installation_form = InstallationForm()

    context = {
        'form': installation_form
    }

    return render(request, 'create_installation.html', context)


def dashboard_modify_installation(request, pk_inst):
    installation = Installation.objects.get(pk=pk_inst)

    if request.method == 'POST':
        installation_form = InstallationForm(request.POST, request.FILES, instance=installation)
        if installation_form.is_valid():
            installation_form.save()
            return redirect('/dashboard/installations')
    else:
        installation_form = InstallationForm(instance=installation)

    context = {
        'installation': installation,
        'form': installation_form
    }

    return render(request, 'modify_installation.html', context)


def dashboard_delete_installation(request, pk_inst):
    installation_selected = Installation.objects.get(pk=pk_inst)
    installation_selected.delete()

    return redirect('/dashboard/installations')
