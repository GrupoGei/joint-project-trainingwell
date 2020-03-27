from django import forms
from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=30)


class Installation(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField()
    capacity = models.IntegerField()
    sports = models.ManyToManyField(Sport, on_delete=models.SET_NULL, related_name='installations')


class Organizer(models.Model):
    num_client = models.CharField(max_length=30)
    password = models.CharField(max_length=30, widget=forms.PasswordInput)


class CurrentReservations(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='current_reservations')


class Reservation(models.Model):
    date = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='reservations')
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, related_name='reservations')
    current_reservations = models.ForeignKey(CurrentReservations, on_delete=models.SET_NULL,
                                             related_name='reservations', null=True)
