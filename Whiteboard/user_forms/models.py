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
    '''
    Track the current download session of the user.
    '''
    cnet_id = models.CharField(max_length = 42)
    date = models.DateTimeField('date published', default = timezone.now)
    year = models.IntegerField(default=datetime.date.today().year)
    people_only = models.BooleanField(default = False)
    repeat_user = models.BooleanField(default = False)

    def __str__(self):
        return str(self.cnet_id)


class Course(models.Model):
    sessions = models.ManyToManyField(Session) # Don't worry about this Andy.
    name = models.CharField(max_length = 200, blank = True)
    quarter = models.CharField(max_length = 42)
    dept = models.CharField(max_length = 4)
    year = models.IntegerField()

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    courses_in = models.ManyToManyField(Course)
    first_name = models.CharField(max_length = 42, blank = True)
    last_name = models.CharField(max_length = 42, blank = True)
    email = models.CharField(max_length = 100, blank = True)
    cnet_id = models.CharField(max_length = 42, blank = True)
    program = models.CharField(max_length = 50, blank = True)
    duplicates = models.BooleanField(default = False, blank = True)


    def full_name(self):
        return str(self.first_name + ' '  + self.last_name)

    def __str__(self):
        return str(self.cnet_id)


class Instructor(models.Model):
    courses_in = models.ManyToManyField(Course)
    title = models.CharField(max_length = 42)
    first_name = models.CharField(max_length = 42)
    last_name = models.CharField(max_length = 42)
    email = models.CharField(max_length = 100)
    duplicates = models.BooleanField(default = False)
    faculty_exchange = models.CharField(max_length = 10)
    phone = models.CharField(max_length = 15)


    def cnet_id(self):
        if '@uchicago.edu' in self.email:
            return re.search(r'^([a-z0-9]*[a-z0-9]?)', self.email).group()
        else:
            return "<Can't confirm CNET ID>"
    
    def full_name(self):
        return str(self.first_name + ' ' + self.last_name)


class Assistant(models.Model):
    courses_in = models.ManyToManyField(Course)
    first_name = models.CharField(max_length = 42)
    last_name = models.CharField(max_length = 42)
    email = models.CharField(max_length = 100)
    cnet_id = models.CharField(max_length = 42)
    program = models.CharField(max_length = 50)
    duplicates = models.BooleanField(default = False)

    def cnet_id(self):
        return re.search(r'^([a-z0-9]*[a-z0-9]?)', self.email).group()

    def full_name(self):
        return str(self.first_name + ' ' + self.last_name)


class File(models.Model):
    course = models.ForeignKey(Course, blank = True)
    heading = models.CharField(max_length = 100, blank = True)
    description = models.TextField(blank = True)
    body = models.TextField(blank = True)
    path = models.CharField(max_length = 300)
    format = models.CharField(max_length = 100)

    # This is a string equivalent of course.id.  This is included because the 
    # library I used for search functionality has trouble narrowing its 
    # 'SearchQuerySet' by foreig key information.  SO i simply clone that 
    # information here.
    classpk = models.CharField(max_length = 300)

    def file_name(self):
        # Extract the filename from the end of the path and return it
        pattern = r'(?<=/)([^/]*)$'
        filename = re.search(pattern, str(self.path))

        if filename != None:
            filename = filename.group()
            return filename
        else:
            return str(self.path)

    def __str__(self):
        return str(self.heading)




