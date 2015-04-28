from django.conf.urls import url

from sensors import views

urlpatterns = [
    url(r'^$', views.verify, name='verify')
]
