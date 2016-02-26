from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


from .forms import DownloadForm, CourseForm, SessionForm
from .models import Session, Course, Student, Instructor, Assistant
from django.views.generic import ListView, DetailView

import random

# import folders 
# Create your views here.

TEST_COURSES_0 = ['STAT 244', 'ENGL 169']
TEST_COURSES_1 = ['CMSC 122', 'MATH 195']
TEST_COURSES_2 = ['SEXY 101', 'FUCK 504']


def get_info(request):
    print('get_info view')
    print()
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session_object = form.save()
            if form.cleaned_data['dl_all']:
                print('Will move directly to post page, everything will be \
                    downloaded')
            else:
                courses_to_confirm = crawler_link(form.cleaned_data, 
                    session_object)
                url = reverse('select_downloads', args=(session_object.id,))
            return HttpResponseRedirect(url)
        else:
            print('form not valid')
            form = SessionForm()
            return render(request, 'user_forms/dl_query.html', {'form': form})
    else:
        form = SessionForm()

    return render(request, 'user_forms/dl_query.html', {'form': form})


def start(request):
    print('At start page')
    return render(request, 'user_forms/start.html')

def view_stats(request):
    print('At view stats page')
    return render(request, 'user_forms/view_stats.html')
 
    

def select_downloads(request, session_id):
    print('select downloads view')
    print()
    print(session_id)
    session = get_object_or_404(Session, pk=session_id)
    
    if request.method == 'POST':

        cnet_pw = request.POST.get('cnet_pw')))
        # Link into crawlers here.
        courses = get_courses(request)
        for course in courses:
            course_model = Course.objects.get(course_id=course)
            course_model.downloaded = True
            course_model.save()

        print('courses should be here: ', courses)
        if not courses:
            return render(request, 'user_forms/select_downloads.html', \
                            {'courses': session.course_set.all(),
                             'error_message': "You didn't choose any courses"})
        else:
            print('courses has stuff in it')
            return HttpResponseRedirect(reverse('post', \
                                            args=(session.id,)))
    else:
        print('Session ID: {}'.format(session_id))
        courses = Course.objects.filter(sessions__id = session_id)
        print('courses should be here', courses)
    return render(request, 'user_forms/select_downloads.html', \
                                                {'courses': courses})


def post(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    all_courses = Course.objects.filter(sessions__cnet_id = session.cnet_id).distinct()
    return render(request, 'user_forms/post.html',
                    {'cnet_id': session.cnet_id,
                      'courses': session.course_set.filter(downloaded=True),
                      'all_courses': all_courses})

def get_courses(request):
    courses = []
    for i in range(1, len(request.POST) + 1):
        if request.POST.get('course' + str(i)):
            courses.append(request.POST.get('course' + str(i)))

    return courses

def crawler_link(cleaned_data, session_object):
    '''
    Will function as the connector to Andy and Bonar's crawlers.
    '''

    if cleaned_data['dl_all']:
        dled_default = True
        print('Crawler should attempt to download all classes')
    else:
        dled_default = False

    # print(cleaned_data['cnet_id'])

    # These lines use some simple random stuff to "select" classes.  Remove
    # once the crawlers are online.  
    num = random.randrange(0,3)
    if num == 0:
        test_courses = TEST_COURSES_0
    elif num == 1:
        test_courses = TEST_COURSES_1
    elif num == 2: 
        test_courses = TEST_COURSES_2

    for course in test_courses:
        num_results = Course.objects.filter(course_id = course).count()
        if num_results == 0:
        # {TO DO} Add in more fields 
            course_object = Course(course_id = course, 
                                downloaded = dled_default)
            course_object.save()
        else:
            course_object = Course.objects.get(course_id = course)

        course_object.sessions.add(session_object)

    # Should call actually web crawler from here to obtain list of courses.  
    # For now we will just use TEST_COURSES.  

    return test_courses




class CourseList(ListView):
    model = Course
    context_object_name = 'course_list'

class CourseDetail(DetailView):
    model = Course
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['students'] = Student.objects.filter(courses_in__id = 
            self.kwargs['course_id'])
        return context