from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics

from sensors.serializers import ReadingSerializer
from sensors.models import Reading
from sensors.permissions import IsOwnerOrReadOnly
from sensors.metrics import metrics

from datetime import datetime, timedelta
from django.utils import timezone


# Attempts int conversion on unicode string
# return false if it fails
def int_or_false(unicode_string):
    try:
        coerced_int = int(unicode_string)
        return coerced_int
    except (ValueError, TypeError):
        return False


def add(x, y) :
    return x + y


# Split readings up by hour and averages them
# Works backwards, so the first index is most recent
# Should return list x where len(x) = # hours
def bin_by_hour(readings, hours, start):
    one_hour = timedelta(hours=1)
    last_hour = start - one_hour
    binned_hours = list()

    start, stop = 0, 0
    for hour in range(hours):
        while (len(readings) > stop and
               readings[stop].created > last_hour):
            stop += 1
            continue

        num = stop - start
        if num:
            # Dict comprehension where keys are metrics
            # Values are averages of metrics readings
            # Calculate by reducing list of metric readings
            # Using simple addition method; finally divide by num
            averages = dict((metric, reduce(add, [getattr(reading, metric)
                for reading in readings[start:stop]]) / num)
                for metric in metrics)
        else:
            averages = {'novalue': 'true'}

        averages['time'] = last_hour
        binned_hours.append(averages)
        last_hour -= one_hour
        start = stop

    return binned_hours


class api_root(APIView):
    """
    Returns a list of all readings
    """
    def get(self, request, format=None):
        readings = Reading.objects.all()
        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)


class sensor_reading(APIView):
    """
    Returns a list of readings by a single sensor, or user
    """
    def get(self, request, format=None):
        readings = Reading.objects.all()

        # requesting a sensor by username; url query is sensor
        sensor_name = request.QUERY_PARAMS.get('sensor', None)
        if sensor_name is not None:
            readings = readings.filter(owner__username=sensor_name)

        # requesting a time window; default or None is all data
        hour_query = request.QUERY_PARAMS.get('hours', None)
        # convert the unicode string to int or return False
        hours = int_or_false(hour_query)
        # if hours query not present, return the last hour
        if hour_query is None or not hours:
            hours = 1

        # bin the readings by hour
        now = timezone.now()
        readings = Reading.objects.filter(created__gt=(now -
                                                       timedelta(hours=hours)))
        binned_readings = bin_by_hour(readings, hours, now)
        return Response(binned_readings)


class sensor_recording(generics.CreateAPIView):
    """
    Allows POST operation
    """

    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user
