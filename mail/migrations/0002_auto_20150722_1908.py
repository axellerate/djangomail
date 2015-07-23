# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaildata',
            name='first_name',
            field=models.CharField(default=b'None', max_length=50),
        ),
        migrations.AddField(
            model_name='emaildata',
            name='last_name',
            field=models.CharField(default=b'None', max_length=50),
        ),
    ]
