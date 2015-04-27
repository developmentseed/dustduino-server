from django.db import models
from django.contrib.auth.models import User


class Sensor(models.Model):

    account = models.ForeignKey(User)
    sensor_name = models.CharField('Sensor Name', max_length=250)
    lat = models.FloatField('Latitude', null=True, blank=True)
    lon = models.FloatField('Latitude', null=True, blank=True)
    address = models.TextField('Sensor Address', max_length=250, null=True, blank=True)
    serial = models.CharField('Serial Number', max_length=250, null=True, blank=True)
    description = models.TextField('Description', max_length=250, null=True, blank=True)

    def __unicode__(self):
        return self.sensor_name


class Reading(models.Model):
    sensor = models.ForeignKey(Sensor)
    created = models.DateTimeField(auto_now_add=True)
    pm10 = models.IntegerField(default=0, null=True, blank=True)
    pm25 = models.IntegerField(default=0, null=True, blank=True)
    pm10count = models.IntegerField(default=0, null=True, blank=True)
    pm25count = models.IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.sensor, self.created)


class SensorVerification(models.Model):

    account = models.ForeignKey(User)
    verification_code = models.CharField('Verification Code', max_length=250)
    updated = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s: %s' % (self.account.email, self.verified)
