from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.contrib.auth import get_user_model
from django.views.generic import View
from sensor.retrieve_historical import HistoricalEcgData
from sensor.insert_session import InsertSession

from rest_framework.views import APIView
from rest_framework.response import Response
from sensorWorker.models import EcgData
from sensorWorker.models import Session
from sensorWorker.forms import TransportForm, FinishForm

def home(request):

    return render(request, 'home.html', {
        'date': datetime.now(),
    })

def sensor(request):
    sessions = Session.objects.all()
    if not sessions:
        form = TransportForm()
        return render(request, 'transport.html', {'form': form})
    else:
        latest_added = Session.objects.latest('start_date')
        return render(request, 'sensor.html', {
            'user_id': latest_added.user_id[0:8],
        })

def finish(request, user_id):   
    if(request.method=='POST'):
        form = FinishForm(request.POST)
        if(form.is_valid()):
            origin_hospital = form.cleaned_data['origin']
            destination_hospital = form.cleaned_data['destination']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            notes = form.cleaned_data['notes']
            print(notes)
            print(user_id)
            print(form.cleaned_data)
            session_info = InsertSession(origin_hospital, destination_hospital, start_date, notes)
            session_info.edit_transport_session(end_date, user_id, notes)
            request.method = "GET"
            return render(request, 'home.html',)
    else:
        data = Session.objects.values().filter(user_id__startswith=user_id).first()
        data['end_date'] = datetime.now()
        form = FinishForm(data)
        return render(request, 'finish.html', {'user_id':user_id, 'form': form})

def get_historical_data(request):
	data = {
		"date": datetime.datetime.now(),
		"ecg_value": 900,
	}
	return JsonResponse(data)

def historical(request):
	return render(request, 'historical.html',)

def transport(request):
    if(request.method=='POST'):
        form = TransportForm(request.POST)

        if(form.is_valid()):
            print(form.cleaned_data)
            origin_hospital = form.cleaned_data['origin']
            destination_hospital = form.cleaned_data['destination']
            start_date = form.cleaned_data['start_date']
            if not start_date:
                start_date = datetime.now()
            session_info = InsertSession(origin_hospital, destination_hospital, start_date)
            session_info.insert_transport_session()
            request.method = "GET"
            return render(request, 'sensor.html', {'user_id': session_info.session_id[0:8]})

    else:
        form = TransportForm()

    return render(request, 'transport.html', {'form': form})

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        user_id = 'testid'
        date = datetime(year=2019, month=11, day=11)
        data = HistoricalEcgData.retrieve_data(user_id, date)
        return Response(data)

class search(TemplateView):

    def get(self, request):
        return render(request, 'search.html',)

    def post(self, request):
        form_dict = dict(request.POST)
        post_data = {}
        post_data['user_id'] = form_dict['id'][0]
        post_data['start_date'] = form_dict['startDate'][0]
        post_data['end_date'] = form_dict['endDate'][0]
        post_data['start_time'] = form_dict['startTime'][0]
        post_data['end_time'] = form_dict['endTime'][0]
        validation_check = self.check_if_valid(post_data)
        args = {}
        args['is_valid'] = validation_check['is_valid']
        args['message'] = validation_check['message']
        if args['is_valid']==False:
            return render(request, 'search.html', args) 
        else:
            args['results'] = self.query_database(post_data)
            return render(request, 'search.html', args)

    def check_if_valid(self, post_data):
        validation_check = {}
        if(post_data['user_id']):
            values = Session.objects.all().filter(user_id__startswith=post_data['user_id'])
            if not values:
                validation_check['is_valid'] = False
                validation_check['message'] = "That ID does not exist, please try again"
                return validation_check
        if (post_data['start_date']):
            try:
                if (post_data['start_time']):
                    start_date_time_str = post_data['start_date'] + " " + post_data['start_time']
                    start_date_time = datetime.strptime(start_date_time_str, "%Y-%m-%d %H:%M:%S")
                else:
                    start_date_time_str = post_data['start_date'] + " 0:0:0"
                    start_date_time = datetime.strptime(start_date_time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                validation_check['is_valid'] = False
                validation_check['message'] = "Improper data, please check date and time formats"
                return validation_check
       
        if (post_data['end_date']):
            try:
                if(post_data['end_time']):
                    end_date_time_str = post_data['end_date'] + " " + post_data['end_time']
                    end_date_time = datetime.strptime(end_date_time_str, "%Y-%m-%d %H:%M:%S")
                else:
                    end_date_time_str = post_data['end_date'] + " 0:0:0"
                    end_date_time = datetime.strptime(end_date_time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                validation_check['is_valid'] = False
                validation_check['message'] = "Improper data, please check date and time formats"
                return validation_check

        validation_check['is_valid'] = True
        validation_check['message'] = "Success"
        return validation_check

    def get_datetime_str(self, start_or_end, post_data):
        if post_data[start_or_end + "_date"] != '':
            date_str = post_data[start_or_end+"_date"] + " " + post_data[start_or_end + "_time"]
            date_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        else:
            print(post_data)
            date_str = post_data[start_or_end+"_date"] + " 0:0:0"
            date_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_time

    def query_database(self, post_data):
        if(post_data['user_id'] != '' and post_data['start_date']=='' and post_data['end_date']==''):
            values = Session.objects.all().filter(user_id__startswith=post_data['user_id'])

        elif(post_data['user_id'] != '' and post_data['start_date'] != '' and post_data['end_date']==''):
            start_date_time = self.get_datetime_str("start", post_data)
            values = Session.objects.all().filter(user_id__startswith=post_data['user_id'], start_date=start_date_time)

        elif(post_data['user_id'] != '' and post_data['start_date'] == '' and post_data['end_date']!=''):
            end_date_time = self.get_datetime("end", post_data)
            values = Session.objects.all().filter(user_id__startswith=post_data['user_id'], end_date=end_date_time)

        elif(post_data['user_id'] != '' and post_data['start_date'] != '' and post_data['end_date'] != ''):
            start_date_time = self.get_datetime_str("start", post_data)
            end_date_time = self.get_datetime_str("end", post_data)
            values = Session.objects.all().filter(user_id__startswith=post_data['user_id'], start_date=start_date_time, end_date=end_date_time)

        elif(post_data['user_id'] == '' and post_data['start_date'] != '' and post_data['end_date']==''):
            start_date_time = self.get_datetime_str("start", post_data)
            values = Session.objects.all().filter(start_date=start_date_time)

        elif(post_data['user_id'] == '' and post_data['start_date'] == '' and post_data['end_date']!=''):
            end_date_time = self.get_datetime("end", post_data)
            values = Session.objects.all().filter(end_date=end_date_time)

        elif(post_data['user_id'] == '' and post_data['start_date'] != '' and post_data['end_date'] != ''):
            start_date_time = self.get_datetime_str("start", post_data)
            end_date_time = self.get_datetime_str("end", post_data)
            values = Session.objects.all().filter(start_date=start_date_time, end_date=end_date_time)
        else:
            values = Session.objects.all()

        data = self.make_data_dictionary_list(values)
        print(data)
        return data
    
    def make_data_dictionary_list(self, values):
        data = []
        for data_entry in values:
            row_dict = {}
            row_dict['user_id'] = data_entry.user_id
            try:
                row_dict['start_date'] = datetime.strftime(data_entry.start_date, "%Y-%m-%d")
            except TypeError:
                row_dict['start_date'] = ''
            try:
                row_dict['start_time'] = datetime.strftime(data_entry.start_date, "%H:%M:%S")
            except TypeError:
                row_dict['start_time'] = ''
            try:    
                row_dict['end_date'] = datetime.strftime(data_entry.end_date, "%Y-%m-%d")
            except TypeError:
                row_dict['end_date'] = ''
            try:
                row_dict['end_time'] = datetime.strftime(data_entry.end_date, "%H:%M:%S")
            except:
                row_dict['end_time'] = ''
            
            data.append(row_dict)
        return data
