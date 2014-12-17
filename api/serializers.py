from rest_framework import serializers
from api.models import Reading
from django.contrib.auth.models import User

import datetime

class ReadingSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Reading
        fields = ('url', 'pm10', 'pm25', 'pm10count', 'pm25count','created', 'owner','createdHour')

    def create(self, validated_data):
        return Reading.objects.create(**validated_data)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    readings = serializers.HyperlinkedRelatedField(many=True, view_name='reading-detail', read_only=True)

    class Meta: 
        model = User
        fields = ('url', 'username', 'password', 'email', 'readings')
        write_only_fields = ('password',)
