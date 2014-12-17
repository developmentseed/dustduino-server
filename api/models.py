from django.db import models
from django.utils.timezone import now

class Reading(models.Model):
    # Authenticating on user
    owner = models.ForeignKey('auth.User', related_name='readings',
                              default='')

    # When the row gets made
    created = models.DateTimeField(auto_now_add=True)
    createdHour = models.DateTimeField(default = datetime.datetime.now, blank=True)

    # Data on sensor readings
    # TODO how do you programmatically set these fields?
    pm10 = models.IntegerField(default = 0)
    pm25 = models.IntegerField(default = 0)
    pm10count = models.IntegerField(default = 0)
    pm25count = models.IntegerField(default = 0)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        super(Reading, self).save(*args, **kwargs)