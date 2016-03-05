from django.conf.urls import url
from django.contrib import admin

from django.http import HttpResponse

from . import views # have to add this in, to have views.THING down there

urlpatterns = [
    url(r'^session=(?P<session_id>[0-9]+)/cnet_id=(?P<cnet_id>[a-zA-Z0-9]+)/se'
        'lect_downloads/$', 
        views.select_downloads, name='select_downloads'),

    url(r'^session=(?P<session_id>[0-9]+)/post/$', views.post, name='post'),
    url(r'^dl_info$', views.get_chalk_info, name='dl_query'),
    url(r'^view_stats$', views.view_stats, name='view_stats'),

    # List of all courses a user is in or has downloaded
    url(r'^view_courses/(?P<cnet_id>[a-zA-Z0-9]+)$', views.CourseList.as_view()
        , name='view_courses'),

    # Individual Course Information
    url(r'^course(?P<course_id>[0-9]+)/(?P<cnet_id>[a-zA-Z0-9]+)/$', 
        views.CourseDetail.as_view(), name='course_detail'),

    # Plot of all or selected courses for a user
    url(r'^my_classes_plot(?P<cnet_id>[a-zA-Z0-9]+)/(?P<course_ids>.+)/$', 
        views.student_classes_plot, name='student_classes_plot'),

    # Plot of a single course.
    url(r'^single_class_plot(?P<course_id>[0-9]+)$', views.single_class_plot,
        name='single_class_plot'),

    
    url(r'^get_cnet_id/$', views.get_cnet_id, name='get_cnet_id'),
    url(r'^view_student(?P<student_id>[a-zA-Z0-9]+)$', 
        views.StudentDetail.as_view(), name='view_student'),
    url(r'^$', views.start, name='start'),
    ]