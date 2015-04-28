from rest_framework import serializers

from sensors.models import Reading, Sensor


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ['sensor', 'hour_code', 'pm10', 'pm25', 'pm10count', 'pm25count']


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
