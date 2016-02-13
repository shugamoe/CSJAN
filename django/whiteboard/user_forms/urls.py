from django.conf.urls import url
from django.contrib import admin

from django.http import HttpResponse

from . import views # have to add this in, to have views.THING down there

urlpatterns = [
    url(r'^select_downloads$', views.select_downloads),
    url(r'^', views.get_info),
    ]