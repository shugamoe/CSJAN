# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 21:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0022_session_repeat_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='downloaded',
        ),
    ]
