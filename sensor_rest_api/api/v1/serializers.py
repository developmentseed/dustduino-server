from rest_framework import serializers

from sensors.models import Reading, Sensor


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ['sensor', 'hour_code', 'pm10', 'pm25', 'pm10count', 'pm25count']


class SensorSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        context = super(SensorSerializer, self).to_representation(obj)

        context['last_reading'] = Reading.objects.filter(sensor_id=obj.id).order_by('-created').values().first()

        return context

    class Meta:
        model = Sensor
