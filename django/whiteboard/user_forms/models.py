from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms
import datetime
import re
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
    sessions = models.ManyToManyField(Session) # Don't worry about this Andy.
    name = models.CharField(max_length=200, blank=True)
    downloaded = models.BooleanField(default=False)
    quarter = models.CharField(max_length=42)
    dept = models.CharField(max_length=4)
    year = models.IntegerField()

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    courses_in = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    email = models.CharField(max_length=100)
    cnet_id = models.CharField(max_length=42)
    program = models.CharField(max_length=50)


    def full_name(self):
        return str(self.first_name + ' '  + self.last_name)

    def __str__(self):
        return '{}'.format(self.cnet_id)


class Instructor(models.Model):
    Course = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    email = models.CharField(max_length=100)

    def cnet_id(self):
        return re.search("^([\w-]*\w)", self.email).group()
    

class Assistant(models.Model):
    Course = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    email = models.CharField(max_length=100)
    program = models.CharField(max_length=50)

    def cnet_id(self):
        return re.search("^([\w-]*\w)", self.email).group()


class File(models.Model):
    owner = models.ForeignKey(Student)
    heading = models.CharField(max_length=100)
    subheading = models.TextField()
    body = models.TextField(blank = True)
    course = models.CharField(max_length=100)
    path = models.CharField(max_length=300)

    def filename(self):
        # Extract the filename from the end of the path and return it
        pattern = '([\w.-]+\.[\w]+)$'
        filename = re.search(pattern, str(self.path))

        if filename != None:
            filename = filename.group()
            return filename
        else:
            return str(self.path)



