# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0025_auto_20160310_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='course_pk',
            field=models.IntegerField(default=-69),
            preserve_default=False,
        ),
    ]
