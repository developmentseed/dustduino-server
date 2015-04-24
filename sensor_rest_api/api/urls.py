from django.conf.urls import url, include
from api.views import ReadingViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'readings', ReadingViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]