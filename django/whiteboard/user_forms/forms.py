from django import forms
from datetime import date
from django.forms import ModelForm
from datetime import datetime
from .models import Session, Course, Student, Instructor, Assistant

QUARTER_CHOICES = (('Fall', 'Fall'), ('Winter', 'Winter'), \
                                    ('Spring', 'Spring'), ('Summer', 'Summer'))
TEST_CLASSES = ['Class 1', 'Class 2']

class DownloadForm(forms.Form):
    cnet_id = forms.CharField(label='CNET ID', max_length = 100)
    cnet_password = forms.CharField(label='CNET password', \
                                                    widget=forms.PasswordInput)
    class_year = forms.IntegerField(label = 'Class year', \
                                                     initial=datetime.now().year)
    quarter = forms.ChoiceField(label = 'Class quarter', \
                                choices=QUARTER_CHOICES)
    dl_all = forms.BooleanField()


class SessionForm(ModelForm):
    quarter = forms.MultipleChoiceField(label='Quarter(s)', \
                                     choices=QUARTER_CHOICES, required = False)
    year = forms.IntegerField(label='Course year', \
                          initial=datetime.now().year, required = False)
    cnet_pw = forms.CharField(label='CNET Password', widget=forms.PasswordInput)
    cnet_id = forms.CharField(label='CNET ID')
    dl_all = forms.BooleanField(label='Download All Chalk Classes',
        required=False)
    class Meta:
        model = Session
        fields = ['cnet_id','cnet_pw', 'quarter', 'year']


class CourseForm(ModelForm):

    class Meta:
        model = Course
        fields = ['downloaded']




