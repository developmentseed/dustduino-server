from django.conf.urls import patterns, url, include
from sensors import views

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
    # list of all readings
    url(r'^all', views.api_root.as_view()),

    # list of all readings from a single sensor
    url(r'^readings/$', views.sensor_reading.as_view()),

    # put method to update data
    url(r'^record', views.sensor_recording.as_view()),

    # log-in
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
