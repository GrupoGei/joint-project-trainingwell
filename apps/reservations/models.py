from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import date, timedelta, datetime


class Sport(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Installation(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    image = models.ImageField(blank=True)
    capacity = models.IntegerField()
    sports = models.ManyToManyField(Sport, related_name='installations')
    price_base = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class RangeHours(models.Model):

    hours = settings.GLOBAL_SETTINGS.get('HOURS_AVAILABLE')
    start_hour = models.IntegerField(choices=hours)
    end_hour = models.IntegerField(choices=hours)

    def __str__(self):
        return str(self.hours[int(self.start_hour)][1]) + '-' + str(self.hours[int(self.end_hour)][1])

    def save(self, *args, **kwargs):
        if self.start_hour > self.end_hour:
            raise ValidationError("L'hora d'inici no pot superar la hora final.")
        else:
            super(RangeHours, self).save(*args, **kwargs)

    def get_time_reserved(self):
        return self.end_hour-self.start_hour


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    teams = models.ManyToManyField('Team', related_name='events', blank=True)

    def __str__(self):
        return self.name

    def print_teams(self):
        teams = Team.objects.filter(events=self)
        result = ""
        i = 0
        for team in teams:
            result += team.name
            i += 1
            if i < len(teams):
                result += ", "
        return result


class Reservation(models.Model):
    day = models.DateField()
    range_hours = models.ForeignKey(RangeHours, on_delete=models.SET_NULL, null=True, related_name='reservation')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, related_name='reservations')
    price = models.FloatField(blank=True, null=True)
    in_shopping_cart = models.BooleanField(default=True)
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='reservation', null=True)

    def __str__(self):
        return "Reserva de " + self.organizer.username + ", dia " + str(self.day)

    def calculate_price(self):
        self.price = self.range_hours.get_time_reserved() * self.installation.price_base * settings.GLOBAL_SETTINGS.get('IVA_TAX')
        if self.installation.discount is not None:
            self.price = self.price * (1-(self.installation.discount/100))

    def take_out_from_cart(self):
        self.in_shopping_cart = False

    def delete(self, *args, **kwargs):
        if self.event:
            self.event.delete(*args, **kwargs)
        super(Reservation, self).delete(*args, **kwargs)


class Team(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


def get_key(list, val):
    for item in list:
        if item[1] == val:
            return item[0]

