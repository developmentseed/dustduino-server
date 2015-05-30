from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=settings.DOCS_URL)),
    url(r'^api/v1/', include('api.v1.urls')),
    url(r'^verify/', include('sensors.urls')),
)
