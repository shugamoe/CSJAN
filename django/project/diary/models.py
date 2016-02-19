from __future__ import unicode_literals

from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=64)
    calories = models.IntegerField()


    def __repr__(self):
        return 'Food({}, {})'.format(self.name, self.calories)

    def __str__(self):
        return '{}, {}'.format(self.name, self.calories)
