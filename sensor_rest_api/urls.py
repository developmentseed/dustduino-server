from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='http://docs.sensorrestapi.apiary.io/#reference')),
    url(r'^api/v1/', include('api.v1.urls')),
    url(r'^verify/', include('sensors.urls')),
)
