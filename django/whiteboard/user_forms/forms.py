from django import forms
from datetime import date
from django.forms import ModelForm
from datetime import datetime
from .models import Session, Course, Student, Instructor, Assistant
from django.utils.safestring import mark_safe

QUARTER_CHOICES = (('Fall', 'Fall'), ('Winter', 'Winter'), \
                                    ('Spring', 'Spring'), ('Summer', 'Summer'))
TEST_CLASSES = ['Class 1', 'Class 2']


# Form for the dl_query template.  This is where the user enters information
# to begin the process of finding classes and downloading that information
# from Chalk.
class SessionForm(ModelForm):
    quarter = forms.MultipleChoiceField(label='Quarter(s)', \
                                     choices=QUARTER_CHOICES, required = False)
    year = forms.IntegerField(label='Course year', \
                          initial=datetime.now().year, required = False)
    cnet_pw = forms.CharField(label='CNET Password', widget=forms.PasswordInput)
    cnet_id = forms.CharField(label='CNET ID')
    people_only = forms.BooleanField(label='Retrieve Demographic Information'\
        ' Only',
        required=False)

    class Meta:
        model = Session
        fields = ['cnet_id','cnet_pw', 'quarter', 'year', 'people_only']


# Dynamic form for filtering the list of students on the individual course 
# page by their major.
class FilterMajorForm(forms.Form):
    def __init__(self, *args, **kwargs):
        majors_list = kwargs.pop('majors_list', None)
        super(FilterMajorForm, self).__init__(*args, **kwargs)

        major_choices = []
        for major in majors_list:
            # Major_choices list needs to be a list of tuples.
            major_choices.append((major, major))

        label = mark_safe("<b>Filter Students By Major</b>")
        self.fields['major_filters'] = forms.MultipleChoiceField(label = label,
         choices = major_choices, required = False)










