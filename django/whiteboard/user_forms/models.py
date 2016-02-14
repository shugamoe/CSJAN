from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Session(models.Model):
    username = models.CharField(max_length=42)
    date = models.DateTimeField('date published')


class Class(models.Model):
    Session = models.ForeignKey(Session)
    course_id = models.CharField(max_length=200)
    quarter = models.CharField(max_length=42)
    year = models.IntegerField(default=date.today().year)
