# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0021_auto_20160306_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='repeat_user',
            field=models.BooleanField(default=False),
        ),
    ]
