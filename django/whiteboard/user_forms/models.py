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
    date = models.DateTimeField('date published')
    quarter = models.CharField(max_length=42)
    year = models.IntegerField(default=datetime.date.today().year)

    def __str__(self):
        return (self.cnet_id, self.date)


class Class(models.Model):
    Session = models.ForeignKey(Session)
    course_id = models.CharField(max_length=200)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return (self.Session, self.course_id, self.downloaded)
    


class SessionForm(ModelForm):
    quarter = forms.ChoiceField(choices=QUARTER_CHOICES)
    year = forms.IntegerField(label = 'Class year', initial=datetime.date.today().year)
    cnet_pw = forms.CharField(label='CNET password', widget=forms.PasswordInput)
    class Meta:
        model = Session
        fields = ['cnet_id','cnet_pw', 'quarter', 'year']


class ClassForm(ModelForm):

    class Meta:
        model = Class
        fields = ['downloaded']