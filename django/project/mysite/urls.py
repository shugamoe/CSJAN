"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.http import HttpResponse

def abc(request):
    path = request.path
    # GET is the http function GET, which returns a dictionary, .get is the 
    # dictionary function .get().
    name = request.GET.get('name', '(no name)') # (no name) is the default value
    return HttpResponse('''
        <h1?Title</h1>
        <p>Welcome! You came to {}.  Your name is {}.</p>
        '''.format(path,name))


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^diary', include('diary.urls')),
]

# r up there means "raw string"
# r'^abc' only matches if it starts with abc

# r'^abc/$' only means we only want 'abc' /$ means if it ends in abc, ^ means
# that it is in the beginning

# r'^$' is the root of the website.  

# url patterns is sorted by priority, first in, first accessed.