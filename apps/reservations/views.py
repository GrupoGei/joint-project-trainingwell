from django.shortcuts import render, redirect
from .models import *
from datetime import date, timedelta
from .forms import RangeHoursForm
from django.core.exceptions import PermissionDenied

# Create your views here.
def show_installations(request):
    first_date = date.today() + timedelta(days=7)
    installations = Installation.objects.order_by('sports')
    context = {
        'installations': installations,
        'date': first_date,
    }

    return render(request, 'installation_list.html', context)


def reserve_day_hours(request, pk_inst, current_date):
    if current_date < str((date.today()+timedelta(days=7))):
        raise PermissionDenied("Has de reservar amb un marge d'una setmana com a mínim.")
    installation = Installation.objects.get(pk=pk_inst)
    reservations = Reservation.objects.filter(day=current_date)
    range_hours_reserved = RangeHours.objects.none()
    for reservation in reservations:
        range_hours_reserved |= RangeHours.objects.filter(reservation=reservation)

    hours_reserved = get_hours_reserved(range_hours_reserved)
    hours_available = get_hours_available(hours_reserved)
    total_hours = get_total_hours()

    if request.method == 'POST':
        form = RangeHoursForm(request.POST)
        if form.is_valid():
            form.save(True, request.user, hours_available, installation)
            return redirect('index')
    else:
        form = RangeHoursForm()

    context = {
        'installation': installation,
        'date': current_date,
        'reservations': reservations,
        'range_hours': range_hours_reserved,
        'total_hours': total_hours,
        'hours_available': hours_available,
        'hours_reserved': hours_reserved,
        'form': form
    }

    return render(request, 'reservation_page.html', context)


def get_total_hours():
    """
    Returns all hours available to reserve.
    :return: [['9:00', '10:00'], ['10:00', '11:00'], ...]
    """
    hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
    total_hours = []
    for hour in hours:
        total_hours.append(hour[1])

    res = [[total_hours[i], total_hours[i + 1]]
           for i in range(len(total_hours) - 1)]

    res.append([total_hours[len(total_hours)-1], settings.GLOBAL_SETTINGS.get('CLOSURE_HOUR')[1]])

    return res


def get_hours_available(hours_reserved):
    """
    Returns a list of the hours available according to the hours reserved and the total hours.
    :param hours_reserved: ['13:00', '14:00', '15:00', '17:00', '18:00']
    :return: ['9:00', '10:00', '11:00', '12:00', '16:00', '19:00', '20:00']
    """
    total_hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
    hours_available = []

    for hour in list(range(len(settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')))):
        current_hour = total_hours[hour][1]
        if current_hour not in hours_reserved:
            hours_available.append(current_hour)

    return hours_available


def get_hours_reserved(range_hours_reserved):
    """
    Returns a list of the hours reserved according to the reservations made for current date.
    :param range_hours_reserved: QuerySet from RangeHours
    :return: ['13:00', '14:00', '15:00', '17:00', '18:00']
    """
    total_hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
    hours_reserved = []
    for hours in range_hours_reserved:
        h = hours.start_hour
        while h < hours.end_hour:
            hours_reserved.append(total_hours[int(h)][1])
            h += 1
    return hours_reserved
