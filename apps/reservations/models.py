from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings


class Sport(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Installation(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(blank=True)
    capacity = models.IntegerField()
    sports = models.ManyToManyField(Sport, related_name='installations')

    def __str__(self):
        return self.name


class CurrentReservations(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_reservations')

    def __str__(self):
        return 'Reserves de la sessió actual de ' + self.organizer.username + ' ' + self.organizer.username


class RangeHours(models.Model):

    hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
    start_hour = models.IntegerField(choices=hours)
    end_hour = models.IntegerField(choices=hours)

    def __str__(self):
        return "Hora " + str(self.hours[int(self.start_hour)][1]) + '-' + str(self.hours[int(self.end_hour)][1])

    def save(self):
        if self.start_hour > self.end_hour:
            raise ValidationError("L'hora d'inici no pot superar la hora final.")
        else:
            super(RangeHours, self).save()


class Reservation(models.Model):
    day = models.DateField()
    range_hours = models.ForeignKey(RangeHours, on_delete=models.SET_NULL, null=True, related_name='reservation')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, related_name='reservations')
    current_reservations = models.ForeignKey(CurrentReservations, on_delete=models.SET_NULL,
                                             related_name='reservations', null=True, blank=True)

    def __str__(self):
        return "Reserva de " + self.organizer.username + ", dia " + str(self.day)


def get_key(list, val):
    for item in list:
        if item[1] == val:
            return item[0]
