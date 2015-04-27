from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^api/v1/', include('api.v1.urls')),
    url(r'^verify/', include('sensors.urls')),
)
