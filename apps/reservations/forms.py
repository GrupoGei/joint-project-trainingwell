from django import forms
from tempus_dominus.widgets import DatePicker
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'validate','placeholder': 'Nom d\'usuari'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contrasenya'}))

class RangeHoursForm(forms.ModelForm):
    class Meta:
        model = RangeHours
        fields = (
            "start_hour",
            "end_hour"
        )
        labels = {
            "start_hour": "Hora de començament",
            "end_hour": "Hora de finalització"
        }

    def save(self, commit, current_user, current_date, hours_available, installation, pk_event):
        hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
        range_hours = super(RangeHoursForm, self).save(commit=False)
        if range_hours.start_hour >= range_hours.end_hour:
            # TODO: ERROR PAGE
            raise forms.ValidationError("L'hora d'inici no pot superar la hora final, ni ser igual.")
        elif time_collision(range_hours.start_hour, range_hours.end_hour, hours_available):
            # TODO: ERROR PAGE
            raise forms.ValidationError("Rang d'hores no disponible, hi ha col·lisió d'hores.")
        else:
            super(RangeHoursForm, self).save()
            event = Event.objects.get(pk=pk_event)
            reservation = Reservation.objects.create(day=datetime.strptime(current_date, "%d-%m-%Y").strftime("%Y-%m-%d"), range_hours=range_hours, organizer=current_user,
                                                     installation=installation, event=event)

            reservation.calculate_price()
            reservation.save()


def get_key(hours_available_list, val):
    for item in hours_available_list:
        if item[1] == val:
            return item[0]


def get_key_list(hours_available):
    """
    Gets a list of hours and transforms it onto its int values according to
    HOURS_AVAILABLE in GLOBAL SETTINGS.
    Parameters:
    :param hours_available: ['9:00', '10:00', '12:00', ...]

    Returns:
    :return: list: [0, 1, 3, ...]
    """
    total_hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
    result = []
    for elem in hours_available:
        result.append(get_key(total_hours, elem))

    return result


def time_collision(start, end, hours_available):
    """
    Determines if there is a collision between hours range.
    :param start: 1
    :param end: 2
    :param hours_available: ['9:00', '10:00', '11:00', ...]
    :return: bool, True if there is a collision, otherwise, returns False.
    """
    hours_available = get_key_list(hours_available)
    hours_not_available = get_hours_not_available(hours_available)
    hours_to_reserve = get_hours_to_reserve(start, end)
    intersec = intersection(hours_not_available, hours_to_reserve)

    return len(intersec) != 0


def intersection(list1, list2):
    lst3 = [value for value in list1 if value in list2]
    return lst3


def get_hours_to_reserve(start, end):
    """
    Returns the "hours" (its indices actually) that want to be reserved.
    :param start: 2
    :param end: 4
    :return: [2, 3]
    """
    result = []
    h = start
    while h < end:
        result.append(h)
        h += 1
    return result


def get_hours_not_available(hours_available):
    """
    Returns the "hours" (its indices actually) that are already reserved.
    :param hours_available: [0, 1, 2, 5]
    :return: [3, 4]
    """
    total_hours_keys = list(range(len(settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE'))))
    hours_not_available = []
    for h in total_hours_keys:
        if h not in hours_available:
            hours_not_available.append(h)
    return hours_not_available


class DateForm(forms.Form):
    date_field = forms.DateField(
        widget=DatePicker(
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            },
        ),
        label='Cerca disponibilitat en una altra data'
    )

    def clean_date_field(self):
        return self.cleaned_data['date_field']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'name',
            'description',
            'teams'
        )
        labels = {
            'name': "Nom de l'esdeveniment",
            'description': "Descripció"
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            'name',
        )
        labels = {
            'name': "Nom de l'equip",
        }
