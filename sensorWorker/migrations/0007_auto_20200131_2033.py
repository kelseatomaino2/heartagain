# Generated by Django 3.0.1 on 2020-01-31 20:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sensorWorker', '0006_auto_20200124_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecgdata',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
