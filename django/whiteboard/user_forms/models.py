from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms
import datetime

QUARTER_CHOICES = (('Fall', 'Fall'), ('Winter', 'Winter'), \
                                    ('Spring', 'Spring'), ('Summer', 'Summer'))

class Session(models.Model):
    cnet_id = models.CharField(max_length=42)
    date = models.DateTimeField('date published', default=timezone.now)
    quarter = models.CharField(max_length=42)
    year = models.IntegerField(default=datetime.date.today().year)

    def __str__(self):
        return str(self.cnet_id)


class Course(models.Model):
    sessions = models.ManyToManyField(Session)
    course_id = models.CharField(max_length=200, blank=True)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return str(self.course_id)


class Student(models.Model):
    courses_in = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    cnet_id = models.CharField(max_length=42)



    # department = models.CharField(max_length=200, blank=True)
    # dept_code = models.CharField(max_length=10, blank=True)
    # year = models.IntegerField(blank=True)
    # quarter = models.CharField(max_length=42, blank=True)


    def get_fullname(self):
        return str(self.first_name + ' '  + self.last_name)

    def __str__(self):
        return '{}'.format(self.cnet_id)


class Instructor(models.Model):
    Course = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    

class Assistant(models.Model):
    Course = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)




