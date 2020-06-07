from django.test import TestCase
from .models import *


class InstallationTestCase(TestCase):
    def setUp(self):
        Installation.objects.create(name='Pista de futbol', description='desc1', capacity=10)

    def test_insert_installation(self):
        installation = Installation.objects.get(name='Pista de futbol')
        self.assertEquals('Pista de futbol', installation.name)

    def test_delete_installation(self):
        Installation.objects.get(name='Pista de futbol').delete()
        installation = Installation.objects.filter(name='Pista de futbol')
        self.assertEquals(0, len(installation))


class SportTestCase(TestCase):
    def setUp(self):
        Sport.objects.create(name='Futbol')

    def test_insert_sport(self):
        sport = Sport.objects.get(name='Futbol')
        self.assertEquals('Futbol', sport.name)

    def test_delete_sport(self):
        Sport.objects.get(name='Futbol').delete()
        sport = Sport.objects.filter(name='Futbol')
        self.assertEquals(0, len(sport))


class RangeHoursTestCase(TestCase):
    def setUp(self):
        RangeHours.objects.create(start_hour=0, end_hour=1)

    def test_insert_RangeHour(self):
        range_hours = RangeHours.objects.get(start_hour=0)
        self.assertEquals(0, range_hours.start_hour)

    def test_delete_RangeHour(self):
        RangeHours.objects.get(start_hour=0).delete()
        range_hours = RangeHours.objects.filter(start_hour=0)
        self.assertEquals(0, len(range_hours))

    def test_incorrect_hour(self):
        with self.assertRaises(ValidationError):
            RangeHours.objects.create(start_hour=3, end_hour=2)


class TeamTestCase(TestCase):
    def setUp(self):
        Team.objects.create(name='BCN team')

    def test_insert_team(self):
        team = Team.objects.get(name='BCN team')
        self.assertEquals('BCN team', team.name)

    def test_delete_team(self):
        Team.objects.get(name='BCN team').delete()
        team = Team.objects.filter(name='BCN team')
        self.assertEquals(0, len(team))


class EventTestCase(TestCase):
    def setUp(self):
        Event.objects.create(name='BCN team partit', description='descr1')

    def test_insert_event(self):
        event = Event.objects.get(name='BCN team partit')
        self.assertEquals('BCN team partit', event.name)

    def test_delete_event(self):
        Event.objects.get(name='BCN team partit').delete()
        event = Event.objects.filter(name='BCN team')
        self.assertEquals(0, len(event))


class ReservationTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user', password='password')
        installation = Installation.objects.create(name='Pista de futbol', description='desc1', capacity=10)
        Reservation.objects.create(day='2020-09-22', price=23.2, in_shopping_cart=False, organizer=user,
                                   installation=installation)

    def test_insert_reservation(self):
        reservation = Reservation.objects.get(organizer=User.objects.get(username='user'))
        self.assertEquals(User.objects.get(username='user'), reservation.organizer)

    def test_delete_reservation(self):
        Reservation.objects.get(organizer=User.objects.get(username='user')).delete()
        reservation = Reservation.objects.filter(organizer=User.objects.get(username='user'))
        self.assertEquals(0, len(reservation))



