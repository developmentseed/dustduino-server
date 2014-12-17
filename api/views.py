from api.models import Reading
from django.contrib.auth.models import User
from django.db.models import Avg
from api.serializers import UserSerializer, ReadingSerializer
from rest_framework import status

from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly

from rest_framework import renderers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

import datetime
import django_filters
from rest_framework import filters

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.parsers import JSONParser
from StringIO import StringIO
import json 

# class ReadingFilter(django_filters.FilterSet):
#     created = django_filters.DateTimeFilter(name="created",lookup_type="gte")
#     class Meta:
#         model = Reading
#         fields = ['created']

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all();
    serializer_class = ReadingSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = ReadingFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,)

    def perform_create(self, serializer):      
        instance = serializer.save(owner = self.request.user)
        hour = instance.created - datetime.timedelta(
            seconds = 60*instance.created.minute + instance.created.second, 
            microseconds = instance.created.microsecond)
        serializer.save(createdHour = hour)

    def get_queryset(self):
        queryset = Reading.objects.all()
        users = self.request.QUERY_PARAMS.get('users', None)
        created = self.request.QUERY_PARAMS.get('created', None)
        if users:
            users = users.split(',')
            queryset = queryset.filter(owner__username__in=users)
        if created:
            date = [int(num) for num in created.split('-')]
            print date
            date = datetime.datetime(date[0],date[1],date[2])
            queryset = queryset.filter(created__gte=date)
        return queryset

    @list_route()
    def aggregate(self, request):
        queryset = self.get_queryset()
        aggData = queryset.values('createdHour').order_by().annotate(
            pm10=Avg('pm10'), 
            pm25=Avg('pm25'), 
            pm10count=Avg('pm10count'), 
            pm25count = Avg('pm25count'))

        data = json.dumps(list(aggData), cls=DjangoJSONEncoder)
        return Response(JSONParser().parse(StringIO(data)))

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        instance = serializer.save(password = self.request.DATA['password'])
        instance.set_password(instance.password)
        instance.save()