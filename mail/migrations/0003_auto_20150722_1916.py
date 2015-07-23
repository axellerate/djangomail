# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_auto_20150722_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaildata',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='emaildata',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]
