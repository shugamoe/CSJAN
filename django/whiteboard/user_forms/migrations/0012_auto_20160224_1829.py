# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0011_auto_20160224_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='in_course',
            new_name='courses_in',
        ),
    ]
