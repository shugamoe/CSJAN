# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_forms', '0005_auto_20160215_0353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=42)),
                ('last_name', models.CharField(max_length=42)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=42)),
                ('last_name', models.CharField(max_length=42)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=42)),
                ('last_name', models.CharField(max_length=42)),
                ('cnet_id', models.CharField(max_length=42)),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='student',
            name='Course',
            field=models.ForeignKey(to='user_forms.Course'),
        ),
        migrations.AddField(
            model_name='instructor',
            name='Course',
            field=models.ForeignKey(to='user_forms.Course'),
        ),
        migrations.AddField(
            model_name='assistant',
            name='Course',
            field=models.ForeignKey(to='user_forms.Course'),
        ),
    ]
