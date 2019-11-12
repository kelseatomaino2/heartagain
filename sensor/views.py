from django.shortcuts import render
from django.http import JsonResponse
import datetime
from django.contrib.auth import get_user_model
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

def home(request):

    return render(request, 'home.html', {
        'date': datetime.datetime.now(),
    })

def sensor(request):
	  return render(request, 'sensor.html', {
        'sensor': '99',
    })

def get_historical_data(request):
	data = {
		"date": datetime.datetime.now(),
		"ecg_value": 900,
	}
	return JsonResponse(data)

def historical(request):
	return render(request, 'historical.html',)

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = {
            "date": datetime.datetime.now(),
            "ecg_value": 900,
        }   
        return Response(data)
