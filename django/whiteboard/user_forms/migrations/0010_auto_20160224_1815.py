# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0009_auto_20160224_1809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='course_id',
            new_name='course',
        ),
    ]
