from django.shortcuts import render

from django.http import HttpResponse

from datetime import datetime
from .forms import UserForm
from .models import SessionForm
# Create your views here.

TEST_CLASSES = ['STAT 244', 'ENGL 169']


def get_info(request):
    classes = {}
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # Might be looking to replace this with a call to url() function.
            return render(request, 'user_forms/select_downloads.html', \
                                                {'classes': form.cleaned_data})
    else:
        form = SessionForm()

    return render(request, 'user_forms/start.html', {'form': form})

def select_downloads(data):
    print('other function')
    return render(request, 'user_forms/select_downloads.html')


