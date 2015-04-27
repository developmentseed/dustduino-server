from rest_framework import serializers

from sensors.models import Reading, Sensor


class ReadingSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Reading

    def create(self, validated_data):
        return Reading.objects.create(**validated_data)


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
