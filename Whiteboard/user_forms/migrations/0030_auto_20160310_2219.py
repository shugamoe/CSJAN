# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0029_auto_20160310_2214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='class_pk',
            new_name='classpk',
        ),
    ]
