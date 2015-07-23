# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0004_cleanedemails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cleanedemails',
            name='attempts_to_contact',
        ),
        migrations.AddField(
            model_name='cleanedemails',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cleanedemails',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
