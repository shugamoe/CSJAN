# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0008_auto_20160222_2343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='Course',
            new_name='course_id',
        ),
    ]
