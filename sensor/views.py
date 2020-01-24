from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
import datetime
from django.contrib.auth import get_user_model
from django.views.generic import View
from .retrieve_historical import HistoricalEcgData

from rest_framework.views import APIView
from rest_framework.response import Response
from sensorWorker.models import EcgData

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
        user_id = 'testid'
        date = datetime.date(year=2019, month=11, day=11)
        data = HistoricalEcgData.retrieve_data(user_id, date)
        return Response(data)

class search(TemplateView):

    def get(self, request):
        values = EcgData.objects.all().filter(user_id='testid')
        print(values)
        return render(request, 'search.html',)

    def post(self, request):
        form_dict = dict(request.POST)
        user_id = form_dict['id'][0]
        start_date = form_dict['start_date'][0]
        end_date = form_dict['end_date'][0]
        start_time = form_dict['start_time'][0]
        end_time = form_dict['end_time'][0]
        args = self.query_database(user_id)
        values = EcgData.objects.all().filter(user_id='testid')
        return render(request, 'search.html', args)

    def query_database(self, user_id=None, start_date=None, end_date=None, start_time=None, end_time=None):
        values = EcgData.objects.all().filter(user_id='testid', date=start_date)
        data = {}
        data['date'] = start_date
        data['user_id'] = user_id
        data['values'] = []
        data['labels'] = []
        for ecg_entry in values:
            x = 0
            data['values'].append(ecg_entry.ecg_value)
            data['labels'].append(x)
        return data
