# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorVerification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('verification_code', models.CharField(max_length=250, verbose_name=b'Verification Code')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('verified', models.BooleanField(default=False)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
