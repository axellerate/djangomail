# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_auto_20150722_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='CleanedEmails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_address', models.CharField(max_length=150)),
                ('mailchimp_bounces', models.IntegerField(default=0)),
                ('mandrill_bounces', models.IntegerField(default=0)),
                ('attempts_to_contact', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
