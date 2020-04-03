from django import forms
from django.contrib.auth.models import User
from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=30)


class Installation(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField()
    capacity = models.IntegerField()
    sports = models.ManyToManyField(Sport, related_name='installations')


class CurrentReservations(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_reservations')


class Reservation(models.Model):
    class AgendaMeta:
        schedule_model = Installation

    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="reservations")
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    approved = models.BooleanField(default=False)
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, related_name='reservations')
    current_reservations = models.ForeignKey(CurrentReservations, on_delete=models.SET_NULL,
                                             related_name='reservations', null=True)




