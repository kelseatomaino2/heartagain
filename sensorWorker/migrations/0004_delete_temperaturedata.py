# Generated by Django 3.0.1 on 2020-01-23 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensorWorker', '0003_pressuredata_temperaturedata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TemperatureData',
        ),
    ]