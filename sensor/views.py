from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
import datetime
from django.contrib.auth import get_user_model
from django.views.generic import View
from .retrieve_historical import HistoricalEcgData
from .search_data import SearchData

from rest_framework.views import APIView
from rest_framework.response import Response

def home(request):

    return render(request, 'home.html', {
        'date': datetime.datetime.now(),
    })

class search(TemplateView):
    def get(self, request):
        form = SearchData()
        return render(request, 'search.html', {'form':form})
    def post(self, request):
        form = SearchData(request.POST)
        if form.is_valid():
            print(form)
            text = form.cleaned_data['post']
            form = HomeForm()
            return redirect('home')
        form_dict = dict(request.POST)
        user_id = form_dict['id'][0]
        args = {'form': form, 'user_id': user_id}
        return render(request, 'search.html', args)


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





