from django.conf.urls import url, include
from django.contrib import admin

from django.http import HttpResponse

from . import views # have to add this in, to have views.THING down there

urlpatterns = [
    url(r'^session=(?P<session_id>[0-9]+)/cnet_id=(?P<cnet_id>[a-zA-Z0-9]+)/se'
        r'lect_downloads/(?P<courses_to_confirm>.+)$', 
        views.select_downloads, name='select_downloads'),
    
    url(r'^session=(?P<session_id>[0-9]+)/post/$', views.post, name='post'),
    url(r'^dl_info$', views.get_chalk_info, name='dl_query'),
    url(r'^browse_classes$', views.browse_classes, name='browse_classes'),

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

    # Obtain uers's CNET ID
    url(r'^get_cnet_id/$', views.get_cnet_id, name='get_cnet_id'),

    # Student Detail Page
    url(r'^view_student(?P<student_id>[0-9]+)$', 
        views.StudentDetail.as_view(), name = 'view_student'),

    # Instructor Detail Page
    url(r'^view_instructor(?P<instructor_id>[0-9]+)$', 
        views.InstructorDetail.as_view(), name = 'view_instructor'),


    # Assistant Detail Page
    url(r'^view_assistant(?P<assistant_id>[0-9]+)$', 
        views.AssistantDetail.as_view(), name = 'view_assistant'),

    # Search pdfs and txt files for single class
    url(r'^search/(?P<course_id>[0-9]+)/$', 
        views.SearchClassFilesView.as_view(), name = 'search_single_class_files'
         ),


    # View a single file
    url(r'^view_file(?P<file_id>[0-9]+)/for_course(?P<course_id>[0-9]+)/query='
        r'(?P<query>.+)/$', views.view_file, name = 'view_file'),


    url(r'^$', views.start, name='start'),
    ]