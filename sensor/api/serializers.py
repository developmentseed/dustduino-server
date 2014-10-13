from django.forms import widgets
from rest_framework import serializers
from api.models import Reading
from django.contrib.auth.models import User

class ReadingSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source='owner.username')
    class Meta:
        model = Reading
        fields = ('created', 'owner', 'pm10', 'pm10_reading',
                  'pm25', 'pm25_reading')
