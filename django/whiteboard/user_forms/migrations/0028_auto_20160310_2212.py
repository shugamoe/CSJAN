# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0027_auto_20160310_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='course_pk',
            field=models.CharField(max_length=300),
        ),
    ]
