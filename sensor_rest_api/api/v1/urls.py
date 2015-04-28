from django.conf.urls import url, include
from api.v1.views import ReadingViewSet, SensorViewSet, register_sensor
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'readings', ReadingViewSet)
router.register(r'sensors', SensorViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register/$', register_sensor)
]
