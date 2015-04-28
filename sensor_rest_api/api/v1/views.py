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
