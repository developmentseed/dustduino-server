from django.conf.urls import patterns, url, include
from api import views

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
    # list of all readings
    url(r'^api/all', views.api_root.as_view()),

    # list of all readings from a single sensor
    url(r'^api/readings/$', views.sensor_reading.as_view()),

    # put method to update data
    url(r'^api/record/(?P<pk>[0-9]+)$', views.sensor_recording.as_view()),
)
