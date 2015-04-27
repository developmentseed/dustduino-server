# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pm10', models.IntegerField(default=0, null=True, blank=True)),
                ('pm25', models.IntegerField(default=0, null=True, blank=True)),
                ('pm10count', models.IntegerField(default=0, null=True, blank=True)),
                ('pm25count', models.IntegerField(default=0, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sensor_name', models.CharField(max_length=250, verbose_name=b'Sensor Name')),
                ('lat', models.FloatField(null=True, verbose_name=b'Latitude', blank=True)),
                ('lon', models.FloatField(null=True, verbose_name=b'Latitude', blank=True)),
                ('address', models.TextField(max_length=250, null=True, verbose_name=b'Sensor Address', blank=True)),
                ('serial', models.CharField(max_length=250, null=True, verbose_name=b'Serial Number', blank=True)),
                ('description', models.TextField(max_length=250, null=True, verbose_name=b'Description', blank=True)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reading',
            name='sensor',
            field=models.ForeignKey(to='sensors.Sensor'),
            preserve_default=True,
        ),
    ]
