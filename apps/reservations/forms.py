from django import forms
from django.conf import settings
from .models import RangeHours


class RangeHoursForm(forms.ModelForm):
    class Meta:
        model = RangeHours
        fields = (
            "start_hour",
            "end_hour"
        )

    def save(self, commit=True):
        hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
        range_hours = super(RangeHoursForm, self).save(commit=False)
        if range_hours.start_hour > range_hours.end_hour:
            # TODO: ERROR PAGE
            raise forms.ValidationError("L'hora d'inici no pot superar la hora final.")
        else:
            super(RangeHoursForm, self).save()


def get_key(list, val):
    for item in list:
        if item[1] == val:
            return item[0]
