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
    duplicates = models.BooleanField(default=False)


    def full_name(self):
        return str(self.first_name + ' '  + self.last_name)

    def __str__(self):
        return '{}'.format(self.cnet_id)


class Instructor(models.Model):
    courses_taught = models.ManyToManyField(Course)
    title = models.CharField(max_length=42)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    email = models.CharField(max_length=100)
    duplicates = models.BooleanField(default=False)
    faculty_exchange = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)


    def cnet_id(self):
        return re.search("^([\w-]*\w)", self.email).group()
    
    def full_name(self):
        return str(self.first_name + ' ' + self.last_name)

class Assistant(models.Model):
    courses_taught = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    email = models.CharField(max_length=100)
    cnet_id = models.CharField(max_length=42)
    program = models.CharField(max_length=50)
    duplicates = models.BooleanField(default=False)

    def cnet_id(self):
        return re.search("^([\w-]*\w)", self.email).group()

    def full_name(self):
        return str(self.first_name + ' ' + self.last_name)


class File(models.Model):
    owner = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    heading = models.CharField(max_length=100, blank = True)
    description = models.TextField(blank = True)
    body = models.TextField(blank = True)
    path = models.CharField(max_length=300)
    format = models.CharField(max_length=10)

    def file_name(self):
        # Extract the filename from the end of the path and return it
        pattern = '([\w.-]+\.[\w]+)$'
        filename = re.search(pattern, str(self.path))

        if filename != None:
            filename = filename.group()
            return filename
        else:
            return str(self.path)

    def __str__(self):
        return str(self.file_name())



