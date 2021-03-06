from django import forms
from datetime import date
from django.forms import ModelForm
from datetime import datetime
from .models import Session, Course, Student, Instructor, Assistant
from django.utils.safestring import mark_safe
from django import forms
from haystack.forms import SearchForm

QUARTER_CHOICES = (('Autumn', 'Autumn'), ('Winter', 'Winter'), \
                                    ('Spring', 'Spring'), ('Summer', 'Summer'))
TEST_CLASSES = ['Class 1', 'Class 2']


# Form for the dl_query template.  This is where the user enters information
# to begin the process of finding classes and downloading that information
# from Chalk.
class SessionForm(ModelForm):
    quarter = forms.MultipleChoiceField(label='Quarter(s) (Optional)', \
                                     choices=QUARTER_CHOICES, required = False)
    year = forms.IntegerField(label='Course year', \
                          initial=datetime.now().year, required = False)
    cnet_pw = forms.CharField(label='CNET Password', widget=forms.PasswordInput)
    cnet_id = forms.CharField(label='CNET ID')

    class Meta:
        model = Session
        fields = ['cnet_id','cnet_pw', 'quarter', 'year']


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


class ClassFilesSearchForm(SearchForm):
    keyword = forms.CharField(required=True)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(ClassFilesSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        # Check to see if a start_date was chosen.
        if self.cleaned_data['keyword']:
            kw = self.cleaned_data['keyword']
            from django.db.models import Q
            sqs = sqs.filter(Q(heading__contains = kw) | 
                Q(description__contains = kw) | Q(body__contains = kw))

        return sqs


class SelectCoursesForm(forms.Form):
    cnet_pw = forms.CharField(label = 'Re-enter CNET Password', widget = 
        forms.PasswordInput, required = True)

    def __init__(self, *args, **kwargs):
        course_list = kwargs.pop('course_list', None)
        super(SelectCoursesForm, self).__init__(*args, **kwargs)

        course_choices = []
        for course in course_list:
            course_choices.append((course, course))

        label = mark_safe("Confirm Course Selection")
        self.fields['course_choices'] = forms.MultipleChoiceField(label = label, 
            choices = course_choices, required = True)

        class Meta:
            fields = ['course_choices', 'cnet_pw']








