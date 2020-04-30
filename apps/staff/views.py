from django.shortcuts import render


def dashboard(request):

    context = {}

    return render(request, 'installation_list_responsible.html', context)
