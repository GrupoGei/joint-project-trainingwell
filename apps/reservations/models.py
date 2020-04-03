from django.db import models
from django.contrib.auth.models import User


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


class Date(models.Model):
    day = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()

    def __str__(self):
        return "Dia " + str(self.day) + " hora " + str(self.start_hour) + '-' + str(self.end_hour)


class Reservation(models.Model):
    date = models.ForeignKey(Date, on_delete=models.SET_NULL, null=True, related_name='reservation')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, related_name='reservations')
    current_reservations = models.ForeignKey(CurrentReservations, on_delete=models.SET_NULL,
                                             related_name='reservations', null=True, blank=True)

    def __str__(self):
        return "Reserva de " + self.organizer.username
