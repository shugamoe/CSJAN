from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

import datetime

class Question(models.Model):
    # Below are fields.  Each Field is an instance of a Field class.
    # Every Field class type (CharField, DateTimeField, etc.) has an optional
    # first argument to designate a human-readable name (for documentation 
    # perhaps).
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    def __str__(self):              # __unicode__ on Python 2
        return self.question_text


class Choice(models.Model):
    # Because we inserted foreign key, the 'set' of Choices can be accessed 
    # from a question object by running 'Question.choice_set.all()' in the 
    # Django shell.
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
        return self.choice_text



class Request(models.Model):
    pass