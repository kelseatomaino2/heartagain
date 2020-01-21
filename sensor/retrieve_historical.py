#from heartagain.models import EcgData
from django.apps import apps
from sensorWorker.models import EcgData

class HistoricalEcgData():

	def retrieve_data(user_id, date):
		EcgData = apps.get_model('sensorWorker', 'EcgData')
		ecg_data = EcgData.objects.all().filter(user_id='testid')
		#print(ecg_data)
		data = {}
		data['date'] = date
		data['user_id'] = user_id
		data['values'] = []
		data['labels'] = []
		for ecg_entry in ecg_data:
			x = 0
			data['values'].append(ecg_entry.ecg_value)
			data['labels'].append(x)
		return data