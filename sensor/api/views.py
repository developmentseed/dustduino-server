from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics

from api.serializers import ReadingSerializer
from api.models import Reading
from api.permissions import IsOwnerOrReadOnly
from api.metrics import metrics

from datetime import datetime, timedelta
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

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
            averages = {}

        averages['time'] = last_hour
        averages['readings'] = num
        binned_hours.append(averages)
        last_hour -= one_hour
        start = stop

    return binned_hours


class ApiRoot(APIView):
    """
    Returns a list of all readings
    """
    def get(self, request, format=None):
        readings = Reading.objects.all()
        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)


class Read(APIView):
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
        readings = readings.filter(created__gt=(now -
                                                timedelta(hours=hours)))
        binned_readings = bin_by_hour(readings, hours, now)
        return Response(binned_readings)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def record(request):
    """
    Listens for PUT operations
    """

    if request.method == 'PUT':
        data = JSONParser().parse(request)

        print request.user

        if request.user.is_authenticated():
            serializer = ReadingSerializer(data=data)
        else:
            print 'no user'

        #if serializer.is_valid():
            #serializer.save()
            #return JSONResponse(serializer.data, status=201)
        #return JSONResponse(serializer.errors, status=400)

        return JSONResponse({}, status=201)


class CreateRecord(generics.CreateAPIView):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user
