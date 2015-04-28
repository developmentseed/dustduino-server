from rest_framework import serializers

from sensors.models import Reading, Sensor


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
