from django.conf.urls import url
from django.contrib import admin

from django.http import HttpResponse

from . import views # have to add this in, to have views.THING down there

urlpatterns = [
    url(r'^session=(?P<session_id>[0-9]+)/select_downloads/$', views.select_downloads, \
                                                    name='select_downloads'),
    url(r'^session=(?P<session_id>[0-9]+)/post/$', views.post, name='post'),
    url(r'^dl_info$', views.get_info, name='dl_query'),
    url(r'^$', views.start, name='start'),    
    ]