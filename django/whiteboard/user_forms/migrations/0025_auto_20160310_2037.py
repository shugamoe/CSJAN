# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0024_auto_20160306_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='course',
            field=models.ForeignKey(blank=True, to='user_forms.Course'),
        ),
        migrations.AlterField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(blank=True, to='user_forms.Student'),
        ),
        migrations.AlterField(
            model_name='student',
            name='cnet_id',
            field=models.CharField(max_length=42, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=42, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=42, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
