from django.shortcuts import render

from django.http import HttpResponse

from datetime import datetime
from .forms import UserForm

# Create your views here.


def get_info(request):
    classes = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # Might be looking to replace this with a call to url() function.
            return render(request, 'user_forms/select_downloads.html', \
                                                {'classes': form.cleaned_data})
    else:
        form = UserForm()

    return render(request, 'user_forms/start.html', {'form': form})

def select_downloads(data):
    print('other function')
    return render(request, 'user_forms/select_downloads.html')


