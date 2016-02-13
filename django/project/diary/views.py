from django.shortcuts import render

from django.http import HttpResponse

from datetime import datetime

def start(request):
    # return HttpResponse('Test')

    c = {'name': 'Julian',
         'foods': ['chicken rice', 'ramen', 'pasta'],
         }
         if request.method == 'POST':
            func(request.GET) 
    return render(request, 'diary/start.html', c) # c is the context


def about(request):
    now = datetime.now()
    return redner(request, 'diary/about.html')

# Create your views here.
