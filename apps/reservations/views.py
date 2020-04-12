from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *
from datetime import date, timedelta, datetime
from .forms import RangeHoursForm, DateForm
from django.core.exceptions import PermissionDenied


def show_installations(request):
    first_date = date.today() + timedelta(days=7)
    installations = Installation.objects.order_by('sports')

    context = {
        'installations': installations,
        'date': first_date,
    }

    return render(request, 'installation_list.html', context)


def show_installations_reserved(request, username):
    user_reservations = Reservation.objects.filter(organizer=request.user)

    context = {
        'user_reservations': user_reservations
    }

    return render(request, 'installation_reserved_list.html', context)


def reserve_day_hours(request, pk_inst, current_date):
    installation = Installation.objects.get(pk=pk_inst)
    date_reservations = Reservation.objects.filter(day=datetime.strptime(current_date, "%d-%m-%Y").strftime("%Y-%m-%d"))
    range_hours_reserved = RangeHours.objects.none()

    for reservation in date_reservations:
        range_hours_reserved |= RangeHours.objects.filter(reservation=reservation)

    hours_reserved = get_hours_reserved(range_hours_reserved)
    hours_available = get_hours_available(hours_reserved)
    total_hours = get_total_hours()

    context = {
        'installation': installation,
        'date': current_date,
        'date_reservations': date_reservations,
        'range_hours': range_hours_reserved,
        'total_hours': total_hours,
        'hours_available': hours_available,
        'hours_reserved': hours_reserved,
    }

    if request.method == 'POST':
        form = RangeHoursForm(request.POST)
        if form.is_valid():
            form.save(True, request.user, current_date, hours_available, installation)

            return redirect('/show_installations_reserved/'+request.user.username)
    else:
        form = RangeHoursForm()
        date_form = DateForm()

    context['form'] = form
    context['date_form'] = date_form

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


def change_date(request, pk_inst):
    if request.method == 'POST':
        date_form = DateForm(request.POST)
        if date_form.is_valid():
            curr_date = date_form.cleaned_data['date_field']
            curr_date_formatted = str(curr_date.day)+'-'+str(curr_date.month)+'-'+str(curr_date.year)
            return redirect('/reservations/'+str(pk_inst)+'/date/'+curr_date_formatted)