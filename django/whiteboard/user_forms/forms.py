from django import forms
from datetime import date


QUARTER_CHOICES = (('Fall', 'Fall'), ('Winter', 'Winter'), \
                                    ('Spring', 'Spring'), ('Summer', 'Summer'))
TEST_CLASSES = ['Class 1', 'Class 2']

class UserForm(forms.Form):
    cnet_id = forms.CharField(label='CNET ID', max_length = 100)
    cnet_password = forms.CharField(label='CNET password', \
                                                    widget=forms.PasswordInput)
    class_year = forms.IntegerField(label = 'Class year', \
                                                     initial=date.today().year)
    quarter = forms.ChoiceField(label = 'Class quarter', \
                                choices=QUARTER_CHOICES)

class DownloadForm(forms.Form):
    pass





