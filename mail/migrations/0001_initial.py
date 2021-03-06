# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_address', models.CharField(max_length=150)),
                ('hard_bounces', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['email_address'],
                'verbose_name_plural': 'Email Data',
            },
        ),
    ]
