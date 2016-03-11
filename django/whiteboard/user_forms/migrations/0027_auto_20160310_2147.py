# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0026_file_course_pk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='format',
            field=models.CharField(max_length=100),
        ),
    ]
