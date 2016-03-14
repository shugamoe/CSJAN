# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0030_auto_20160310_2219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='owner',
        ),
    ]
