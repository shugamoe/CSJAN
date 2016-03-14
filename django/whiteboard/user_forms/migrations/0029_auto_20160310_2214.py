# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0028_auto_20160310_2212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='course_pk',
            new_name='class_pk',
        ),
    ]
