from django.db import models
from django.utils.timezone import now

class Reading(models.Model):
    # Authenticating on user
    owner = models.ForeignKey('auth.User', related_name='api',
                              default='')

    # When the row gets made
    created = models.DateTimeField(auto_now_add=True)

    # Data on sensor readings
    # TODO how do you programmatically set these fields?
    pm10 = models.IntegerField()
    pm10_reading = models.IntegerField()
    pm25 = models.IntegerField()
    pm25_reading = models.IntegerField()

    class Meta:
        ordering = ('-created',)
