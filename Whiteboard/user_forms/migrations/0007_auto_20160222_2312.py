# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0006_auto_20160222_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assistant',
            name='Course',
        ),
        migrations.AddField(
            model_name='assistant',
            name='Course',
            field=models.ManyToManyField(to='user_forms.Course'),
        ),
        migrations.RemoveField(
            model_name='course',
            name='Session',
        ),
        migrations.AddField(
            model_name='course',
            name='Session',
            field=models.ManyToManyField(to='user_forms.Session'),
        ),
        migrations.RemoveField(
            model_name='instructor',
            name='Course',
        ),
        migrations.AddField(
            model_name='instructor',
            name='Course',
            field=models.ManyToManyField(to='user_forms.Course'),
        ),
        migrations.RemoveField(
            model_name='student',
            name='Course',
        ),
        migrations.AddField(
            model_name='student',
            name='Course',
            field=models.ManyToManyField(to='user_forms.Course'),
        ),
    ]
