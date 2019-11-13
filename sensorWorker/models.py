from django.db import models

# Create your models here.
class EcgData(models.Model):
    user_id = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    ecg_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        app_label = 'sensorWorker'
        db_table = 'ecg_data'