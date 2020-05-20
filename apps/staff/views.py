from collections import defaultdict

from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.reservations.models import *
from apps.staff.forms import InstallationForm, PriceForm, SportForm


def dashboard_installations(request):
    installations = Installation.objects.all()
    sports = Sport.objects.all()

    context = {
        'installations': installations,
        'sports': sports
    }

    return render(request, 'installation_list_staff-resp.html', context)


def dashboard_filtered_installations(request, sport):
    installations = Installation.objects.filter(sports__name=sport)
    sports = Sport.objects.all()
    context = {
        'installations': installations,
        'sports': sports
    }

    return render(request, 'installation_list_staff-resp.html', context)


def dashboard_reserves(request):
    if 'organizer' in request.GET:
        if request.GET['organizer'] != '':
            reserves = Reservation.objects.filter(organizer__username=request.GET['organizer'])
        else:
            reserves = Reservation.objects.all()
    else:
        reserves = Reservation.objects.all()

    context = {
       'reserves': reserves,
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


def dashboard_filtered_organizers(request, username):
    reserves = Reservation.objects.filter(organizer__username=username)

    context = {
        'reserves': reserves
    }

    return render(request, 'reserves_list_staff.html', context)


def dashboard_reports(request):
    context = {}

    return render(request, 'reports.html', context)


def dashboard_manage_prices(request):
    installations = Installation.objects.all()
    sports = Sport.objects.all()

    context = {
        'installations': installations,
        'sports': sports
    }

    return render(request, 'installation_list_staff-manag.html', context)


def dashboard_filtered_installations_prices(request, sport):
    installations = Installation.objects.filter(sports__name=sport)
    sports = Sport.objects.all()
    context = {
        'installations': installations,
        'sports': sports
    }

    return render(request, 'installation_list_staff-manag.html', context)


def dashboard_modify_price(request, pk_inst):
    installation = Installation.objects.get(pk=pk_inst)

    if request.method == 'POST':
        price_form = PriceForm(request.POST, instance=installation)
        if price_form.is_valid():
            price_form.save()
            return redirect('/dashboard/prices')
    else:
        price_form = PriceForm(instance=installation)

    context = {
        'installation': installation,
        'form': price_form
    }

    return render(request, 'modify_price.html', context)


def dashboard_create_sport(request):
    if request.method == 'POST':
        sport_form = SportForm(request.POST)
        if sport_form.is_valid():
            sport_form.save()
            return redirect('/dashboard/installations')
    else:
        sport_form = SportForm()

    context = {
        'form': sport_form,
    }

    return render(request, 'create_sport.html', context)

def chart_view(request):
    return render(request, 'charts.html', {})

def get_data(request):

    reservations = Reservation.objects.all()
    data = defaultdict(int)
    for reserva in reservations:
        data[reserva.installation.name] += reserva.range_hours.get_time_reserved()

    return JsonResponse(data)

from rest_framework.views import APIView
from rest_framework.response import Response

class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        reservations = Reservation.objects.all()
        dades = defaultdict(int)
        for reserva in reservations:
            inst_name = reserva.installation.name
            dades[inst_name] += reserva.range_hours.get_time_reserved()

        data = {
            "labels": dades.keys(),
            "default": dades.values()
        }
        return Response(data)