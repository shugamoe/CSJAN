# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0019_auto_20160306_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='format',
            field=models.CharField(default='gay', max_length=10),
            preserve_default=False,
        ),
    ]
