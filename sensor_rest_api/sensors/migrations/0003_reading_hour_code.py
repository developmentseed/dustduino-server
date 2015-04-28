# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0002_sensorverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='reading',
            name='hour_code',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Hour Code', blank=True),
            preserve_default=True,
        ),
    ]
