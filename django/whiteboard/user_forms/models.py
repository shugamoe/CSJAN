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
    Session = models.ForeignKey(Session)
    course_id = models.CharField(max_length=200, blank=True)
    downloaded = models.BooleanField(default=False)

    # department = models.CharField(max_length=200, blank=True)
    # dept_code = models.CharField(max_length=10, blank=True)
    # year = models.IntegerField(blank=True)
    # quarter = models.CharField(max_length=42, blank=True)

    def __str__(self):
        return '{}'.format(self.course_id)


class Student(models.Model):
    Course = models.ForeignKey(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    cnet_id = models.CharField(max_length=42)


class Instructor(models.Model):
    Course = models.ForeignKey(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    

class Assistant(models.Model):
    Course = models.ForeignKey(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)


class SessionForm(ModelForm):
    quarter = forms.MultipleChoiceField(label='quarter(s)', \
                                        choices=QUARTER_CHOICES)
    year = forms.IntegerField(label='Course year', initial=datetime.date.today().year)
    cnet_pw = forms.CharField(label='CNET Password', widget=forms.PasswordInput)
    cnet_id = forms.CharField(label='CNET ID')
    class Meta:
        model = Session
        fields = ['cnet_id','cnet_pw', 'quarter', 'year']


class CourseForm(ModelForm):

    class Meta:
        model = Course
        fields = ['downloaded']

