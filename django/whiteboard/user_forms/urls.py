from django.conf.urls import url
from django.contrib import admin

from django.http import HttpResponse

from . import views # have to add this in, to have views.THING down there

urlpatterns = [
    url(r'^(?P<session_id>[0-9]+)/select_downloads/$', views.select_downloads, \
                                                    name='select_downloads'),
    url(r'^(?P<session_id>[0-9]+)/post/$', views.post, name='post'),
    url(r'^$', views.get_info, name='start'),    
    ]