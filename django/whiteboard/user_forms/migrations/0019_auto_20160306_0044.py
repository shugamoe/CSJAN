# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0018_auto_20160305_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='faculty_exchange',
            field=models.CharField(default='554 RYE', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructor',
            name='phone',
            field=models.CharField(default='1-209-648-1679', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructor',
            name='title',
            field=models.CharField(default='King of Gay', max_length=42),
            preserve_default=False,
        ),
    ]
