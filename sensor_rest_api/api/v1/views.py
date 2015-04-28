import json
import datetime
from StringIO import StringIO

from django.db.models import Avg
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import random_name


from sensors.models import Reading, Sensor, SensorVerification
from api.v1.serializers import SensorSerializer, ReadingSerializer
from api.v1.mailer import VerificaitonEmail


class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        sensor = Sensor.objects.get(account=request.user)
        request.data.__setitem__('sensor', sensor.id)
        print request.data
        return super(ReadingViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.values('hour_code', 'sensor').annotate(pm10=Avg('pm10'),
                                                                   pm25=Avg('pm25'),
                                                                   pm10count=Avg('pm10count'),
                                                                   pm25count=Avg('pm25count'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(queryset)


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):

        return Response({"error": "Not Implemented"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        email = request.data.pop('email')
        if isinstance(email, list):
            email = email[0]

        error = self.verify_email(email)
        if error:
            return error

        try:
            user = User.objects.get(email=email)

            if user.is_active:
                instance = Sensor.objects.get(account=user)
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                return Response({"error": "The sensor associated with %s is not active." % email},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "The email (%s) does not exist" % email},
                            status=status.HTTP_400_BAD_REQUEST)


def verify_email(email):
        # If no email is provided raise an error
        if email:
            try:
                validate_email(email)
                return False
            except ValidationError:
                return Response({"error": "Provide a valid email address."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Insufficient information provided."},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_sensor(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        if isinstance(email, list):
            email = email[0]

        sensor_name = request.POST.get('sensor_name')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        address = request.POST.get('address')
        serial = request.POST.get('serial')
        description = request.POST.get('description')

        error = verify_email(email)
        if error:
            return error

        if not sensor_name:
            sensor_name = random_name.generate_name()

        # If a sensor with the email already exists issue an error
        try:
            user = User.objects.get(email=email)

            return Response({"error": "The email %s is already registered with a sensor" % email},
                            status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            # Creat the new user
            with transaction.atomic():
                username = User.objects.make_random_password(length=10)
                password = User.objects.make_random_password(length=10)

                user = User(username=username, password=password, email=email, is_active=False)
                user.save()

                # Add sensor information
                sensor = Sensor(account=user, sensor_name=sensor_name, lat=lat, lon=lon,
                                address=address, serial=serial, description=description)
                sensor.save()

                # Send Verification email
                verification_code = User.objects.make_random_password(length=40)
                verify = SensorVerification(account=user, verification_code=verification_code)
                verify.save()

                mail = VerificaitonEmail(user.email, verification_code)
                mail.send()

                return Response({
                    'email': user.email,
                    'username': user.username,
                    'id': user.id,
                    'verified': verify.verified,
                    'message': 'New sensor is registered. A verification email is sent to the email provided. ' +
                               'Please verify the sensor.',
                }, status=status.HTTP_201_CREATED)
