import json
import datetime
from StringIO import StringIO

from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.parsers import JSONParser


from api.models import Reading
from api.serializers import UserSerializer, ReadingSerializer
from api.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly


class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        hour = instance.created - datetime.timedelta(seconds=60*instance.created.minute + instance.created.second,
                                                     microseconds=instance.created.microsecond)
        serializer.save(createdHour=hour)

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
            date = datetime.datetime(date[0], date[1], date[2])
            queryset = queryset.filter(created__gte=date)
        return queryset

    @list_route()
    def aggregate(self, request):
        queryset = self.get_queryset()
        aggData = queryset.values('createdHour').order_by().annotate(
            pm10=Avg('pm10'),
            pm25=Avg('pm25'),
            pm10count=Avg('pm10count'),
            pm25coun=Avg('pm25count')
        )

        data = json.dumps(list(aggData), cls=DjangoJSONEncoder)
        return Response(JSONParser().parse(StringIO(data)))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)

    def perform_create(self, serializer):
        instance = serializer.save(password=self.request.DATA['password'])
        instance.set_password(instance.password)
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save(password=self.request.DATA['password'])
        instance.set_password(instance.password)
        instance.save()
