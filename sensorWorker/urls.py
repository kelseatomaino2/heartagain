from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path('', views.sensor, name='sensor.html'),
    # path('sensor/', include('sensorWorker.urls')),
]