# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0007_auto_20160222_2312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='Session',
            new_name='sessions',
        ),
    ]
