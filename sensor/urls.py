"""sensor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sensorWorker import views
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', views.home, name='home'),
    url(r'^sensor/', views.sensor, name='sensor'),
    url(r'^search/', views.search.as_view(), name='search'),
    url(r'^api/historical/$', views.get_historical_data, name='api-historical'),
    url(r'^historical/', views.historical, name='historical'),
    url(r'^transport/', views.transport, name='transport'),
    url(r'^api/chart/historical/$', views.ChartData.as_view()),
    url(r'^finish/(?P<user_id>\w+)/$', views.finish, name='finish'),

]
