from django.conf.urls import url, include
from api.views import ReadingViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'readings', ReadingViewSet)
router.register(r'devices', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
