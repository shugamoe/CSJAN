from django.shortcuts import render

from django.http import HttpResponse

from datetime import datetime
from .forms import UserForm
from .models import SessionForm, ClassForm
# Create your views here.

TEST_CLASSES = ['STAT 244', 'ENGL 169']


def get_info(request):
    classes = {}
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            # Insert code here to interact with crawlers and add session info
            # to the database.
            print(form.cleaned_data)
            # Might be looking to replace this with a call to url() function.
            return render(request, 'user_forms/select_downloads.html', \
                                                {'classes': TEST_CLASSES})
    else:
        form = SessionForm()

    return render(request, 'user_forms/start.html', {'form': form})

def select_downloads(request):
    if request.method == 'POST':
        classes = get_classes(request)
        print('classes should be here: ', classes)
    return render(request, 'user_forms/select_downloads.html', \
                                                {'classes': TEST_CLASSES})


def get_classes(request):
    classes = []
    for i in range(1, len(request.POST) + 1):
        if request.POST.get('class' + str(i)):
            classes.append(request.POST.get('class' + str(i)))

    return classes

