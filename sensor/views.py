from django.shortcuts import render
import datetime

def home(request):

    return render(request, 'home.html', {
        'date': datetime.datetime.now(),
    })

def sensor(request):
	  return render(request, 'sensor.html', {
        'sensor': '99',
    })

def historical(request):
	  return render(request, 'historical.html', {
        'history': 'id:999999999',
    })