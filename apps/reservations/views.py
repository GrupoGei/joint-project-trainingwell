from django.shortcuts import render
from .models import Installation


# Create your views here.
def show_installations(request):

    installations = Installation.objects.order_by('sports')
    context = {
        'installations' : installations,
    }

    return render(request, 'installation_list.html', context)


def reserve_day_hours(request):
    context = {}
    return render(request, 'reservation_page.html', context)