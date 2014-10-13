from django.conf.urls import patterns, url, include
from api import views

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
    # list of all readings
    url(r'^api/all', views.ApiRoot.as_view()),

    # list of all readings from a single sensor
    url(r'^api/readings/$', views.Read.as_view()),

    # put method to update data
    url(r'^api/record/$', views.record),

    url(r'^api/create/$', views.CreateRecord.as_view()),
)
