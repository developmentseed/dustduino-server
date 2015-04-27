from django.conf.urls import url, include
from api.views import ReadingViewSet, SensorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'readings', ReadingViewSet)
router.register(r'sensors', SensorViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
