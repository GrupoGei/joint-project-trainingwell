from django.shortcuts import render, redirect
from .models import *
from datetime import date
from .forms import RangeHoursForm


# Create your views here.
def show_installations(request):

    installations = Installation.objects.order_by('sports')
    context = {
        'installations' : installations,
    }

    return render(request, 'installation_list.html', context)


def reserve_day_hours(request):
    total_hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
    current_date = date.today()
    reservations = Reservation.objects.filter(day=current_date)
    range_hours_reserved = RangeHours.objects.none()
    for reservation in reservations:
        range_hours_reserved |= RangeHours.objects.filter(reservation=reservation)

    hours_reserved = get_hours_reserved(range_hours_reserved)
    hours_available = []

    for hour in list(range(len(settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')))):
        current_hour = total_hours[hour][1]
        if current_hour not in hours_reserved:
            hours_available.append(current_hour)

    if request.method == 'POST':
        form = RangeHoursForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RangeHoursForm()

    context = {
        'date': current_date,
        'reservations': reservations,
        'range_hours': range_hours_reserved,
        'hours_available': hours_available,
        'form': form
    }

    return render(request, 'reservation_page.html', context)


def get_hours_reserved(range_hours_reserved):
    available_hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
    hours_reserved = []
    for hours in range_hours_reserved:
        h = hours.start_hour
        while h < hours.end_hour:
            hours_reserved.append(available_hours[int(h)][1])
            h += 1
    return hours_reserved
