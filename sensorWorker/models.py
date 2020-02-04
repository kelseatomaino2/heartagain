from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Session(models.Model):
	user_id = models.CharField(max_length=100)
	start_date = models.DateTimeField(default=timezone.now)
	end_date = models.DateTimeField(null=True, blank=True)
	origin = models.CharField(max_length=100)
	destination = models.CharField(max_length=100)

	class Meta:
		app_label = 'sensorWorker'
		db_table = 'session_info'

class EcgData(models.Model):
    user_id = models.CharField(max_length=100)
    date_time = models.DateTimeField(null=True, blank=True)
    ecg_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        app_label = 'sensorWorker'
        db_table = 'ecg_data'

class FlowData(models.Model):
    user_id = models.CharField(max_length=100)
    date_time = models.DateTimeField(null=True, blank=True)
    flow_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        app_label = 'sensorWorker'
        db_table = 'flow_data'

class PressureData(models.Model):
    user_id = models.CharField(max_length=100)
    date_time = models.DateTimeField(null=True, blank=True)
    pressure_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        app_label = 'sensorWorker'
        db_table = 'pressure_data'

class TemperatureData(models.Model):
    user_id = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    temperature_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        app_label = 'sensorWorker'
        db_table = 'temperature_data'

