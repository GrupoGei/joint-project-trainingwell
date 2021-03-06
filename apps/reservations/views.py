from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *
from datetime import date, timedelta, datetime
from .forms import RangeHoursForm, DateForm, EventForm, TeamForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout


@login_required
def show_installations(request):
    installations = Installation.objects.order_by('sports')
    sports = Sport.objects.all()

    context = {
        'installations': installations,
        'sports': sports
    }

    return render(request, 'installation_list.html', context)


@login_required
def show_installations_reserved(request, username):
    user_reservations = Reservation.objects.filter(organizer=request.user, in_shopping_cart=True)

    context = {
        'user_reservations': user_reservations,
        'num_reservations': len(user_reservations)
    }

    return render(request, 'installation_reserved_list.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def reserve_day_hours(request, pk_inst, current_date, pk_event):

    if str(datetime.strptime(current_date, "%d-%m-%Y").strftime("%Y-%m-%d")) < str((date.today() + timedelta(days=7))):
        # TODO: ERROR PAGE
        raise ValidationError("La reserva de dies només es pot fer amb una setmana d'antelació.")
    installation = Installation.objects.get(pk=pk_inst)
    date_reservations = Reservation.objects.filter(day=datetime.strptime(current_date, "%d-%m-%Y").strftime("%Y-%m-%d"), installation=installation)
    range_hours_reserved = RangeHours.objects.none()
    event = Event.objects.get(pk=pk_event)

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
        'event': event
    }

    if request.method == 'POST':
        form = RangeHoursForm(request.POST)
        if form.is_valid():
            form.save(True, request.user, current_date, hours_available, installation, pk_event)

            return redirect('/show_installations_reserved/' + request.user.username)
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

    res.append([total_hours[len(total_hours) - 1], settings.GLOBAL_SETTINGS.get('CLOSURE_HOUR')[1]])

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


@login_required
def change_date(request, pk_inst, pk_event):
    if request.method == 'POST':
        date_form = DateForm(request.POST)
        if date_form.is_valid():
            curr_date = date_form.cleaned_data['date_field']
            curr_date_formatted = str(curr_date.day) + '-' + str(curr_date.month) + '-' + str(curr_date.year)
            return redirect('/reservations/' + str(pk_inst) + '/date/' + curr_date_formatted + '/event/' + str(pk_event))


@login_required
def delete_reserve(request, pk_reserve):
    reserve_selected = Reservation.objects.get(pk=pk_reserve)
    reserve_selected.delete()

    return redirect('/show_installations_reserved/' + request.user.username)


@login_required
def cancel_reserves_cart(request, username):
    user_reservations = Reservation.objects.filter(organizer=request.user, in_shopping_cart=True)

    for reservation in user_reservations:
        reservation.delete()

    return redirect('/show_installations/')


@login_required
def formalize_reserves(request, username):
    user_reservations = Reservation.objects.filter(organizer=request.user, in_shopping_cart=True)

    for reservation in user_reservations:
        reservation.take_out_from_cart()
        reservation.save()

    context = {
        'username': username
    }

    return render(request, 'thanks_page.html', context)


@login_required
def checkout(request, username):
    session_reservations = Reservation.objects.filter(organizer=request.user, in_shopping_cart=True)
    total_price = 0
    for reservation in session_reservations:
        total_price += reservation.price

    context = {
        'total_price': total_price,
        'username': username,
        'num_reservations': len(session_reservations)
    }

    return render(request, 'checkout.html', context)


@login_required
def filtered_installations(request, sport):
    first_date = date.today() + timedelta(days=7)
    installations = Installation.objects.filter(sports__name=sport)
    sports = Sport.objects.all()

    context = {
        'installations': installations,
        'date': first_date,
        'sports': sports
    }

    return render(request, 'installation_list.html', context)


def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.groups.filter(name='Responsible').exists():
        return redirect('/dashboard/installations')
    elif request.user.groups.filter(name='Manager').exists():
        return redirect('/dashboard/report_util')
    else:
        return redirect('/show_installations/')


@login_required
def show_reserves(request, username):
    if 'team' in request.GET:
        if request.GET['team'] != '':
            reserves = Reservation.objects.filter(event__teams__name__contains=request.GET['team'], organizer__username=username)
        else:
            reserves = Reservation.objects.filter(organizer__username=username)
    elif 'date' in request.GET:
        if request.GET['date'] != '':
            reserves = Reservation.objects.filter(organizer__username=username, day=request.GET['date'])
        else:
            reserves = Reservation.objects.filter(organizer__username=username)
    else:
        reserves = Reservation.objects.filter(organizer__username=username)

    sports = Sport.objects.all()
    date_form = DateForm()

    context = {
        'reserves': reserves,
        'sports': sports,
        'date_form': date_form
    }

    return render(request, 'reserves_list.html', context)


@login_required
def filtered_reserves(request, username, sport):
    if 'team' in request.GET:
        if request.GET['team'] != '':
            reserves = Reservation.objects.filter(event__teams__name__contains=request.GET['team'], organizer__username=username, installation__sports__name__contains=sport)
        else:
            reserves = Reservation.objects.filter(organizer__username=username, installation__sports__name__contains=sport)
    elif 'date' in request.GET:
        if request.GET['date'] != '':
            reserves = Reservation.objects.filter(organizer__username=username, day=request.GET['date'], installation__sports__name__contains=sport)
        else:
            reserves = Reservation.objects.filter(organizer__username=username, installation__sports__name__contains=sport)
    else:
        reserves = Reservation.objects.filter(organizer__username=username, installation__sports__name__contains=sport)
    sports = Sport.objects.all()

    context = {
        'reserves': reserves,
        'sports': sports
    }

    return render(request, 'reserves_list.html', context)


def event_detail(request, pk_event):
    event = Event.objects.get(pk=pk_event)

    context = {
        'event': event,
    }

    return render(request, 'event_detail.html', context)


@login_required
def create_event(request, pk_inst):
    first_date = date.today() + timedelta(days=7)
    first_date = datetime.strptime(str(first_date), "%Y-%m-%d").strftime("%d-%m-%Y")
    installation = Installation.objects.get(pk=pk_inst)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('/reservations/'+str(pk_inst)+'/date/'+str(first_date)+'/event/'+str(event.pk))
    else:
        form = EventForm()

    context = {
        'form': form,
        'installation': installation
    }

    return render(request, 'create_event.html', context)


@login_required
def create_team(request, pk_inst):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/create_event/'+str(pk_inst))
    else:
        form = TeamForm()

    context = {
        'form': form,
    }

    return render(request, 'create_team.html', context)


@login_required
def cancel_reserve(request, pk_reserve):
    reserve_selected = Reservation.objects.get(pk=pk_reserve)
    reserve_selected.delete()

    return redirect('/show_reserves/'+str(request.user.username))


def presentation_page(request):
    return render(request, 'presentation.html')


def current_planning(request):
    if 'team' in request.GET:
        if request.GET['team'] != '':
            reserves = Reservation.objects.filter(event__teams__name__contains=request.GET['team'], day__gte=date.today())
        else:
            reserves = Reservation.objects.filter(day__gte=date.today())
    elif 'date' in request.GET:
        if request.GET['date'] != '':
            reserves = Reservation.objects.filter(day__gte=date.today(), day=request.GET['date'])
        else:
            reserves = Reservation.objects.filter(day__gte=date.today())
    else:
        reserves = Reservation.objects.filter(day__gte=date.today())

    sports = Sport.objects.all()
    date_form = DateForm()

    context = {
        'reserves': reserves,
        'sports': sports,
        'date_form': date_form
    }

    return render(request, 'current_planning.html', context)


def filtered_events(request, sport):
    if 'team' in request.GET:
        if request.GET['team'] != '':
            reserves = Reservation.objects.filter(event__teams__name__contains=request.GET['team'], day__gte=date.today())
        else:
            reserves = Reservation.objects.filter(day__gte=date.today(), installation__sports__name__contains=sport)
    elif 'date' in request.GET:
        if request.GET['date'] != '':
            reserves = Reservation.objects.filter(day__gte=date.today(), day=request.GET['date'])
        else:
            reserves = Reservation.objects.filter(day__gte=date.today(), installation__sports__name__contains=sport)
    else:
        reserves = Reservation.objects.filter(day__gte=date.today(), installation__sports__name__contains=sport)

    sports = Sport.objects.all()
    date_form = DateForm()

    context = {
        'reserves': reserves,
        'sports': sports,
        'date_form': date_form
    }

    return render(request, 'current_planning.html', context)

