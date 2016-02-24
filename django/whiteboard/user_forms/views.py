from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


from .forms import DownloadForm, CourseForm, SessionForm
from .models import Session, Course, Student, Instructor, Assistant

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
            print('session object ID should be here', session_object.id)
            # Insert code here to interact with crawlers and add session info
            # to the database.
            courses = crawler_link(form.cleaned_data, session_object)
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
    

def select_downloads(request, session_id):
    print('select downloads view')
    print()
    print(session_id)
    session = get_object_or_404(Session, pk=session_id)
    
    if request.method == 'POST':


        # We obtain a list of the 
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
        print('Crawler should attempt to download all classes')

    num = random.randrange(0,3)
    print(cleaned_data['cnet_id'])

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
            course_object = Course(course_id = course)
            course_object.save()
        else:
            course_object = Course.objects.get(course_id = course)

        course_object.sessions.add(session_object)

    # Should call actually web crawler from here to obtain list of courses.  
    # For now we will just use TEST_COURSES.  

    return test_courses




# class Session(models.Model):
#     cnet_id = models.CharField(max_length=42)
#     date = models.DateTimeField('date published')
#     quarter = models.CharField(max_length=42)
#     year = models.IntegerField(default=datetime.date.today().year)

#     def __str__(self):
#         return (self.cnet_id, self.date)


# class Course(models.Model):
#     Session = models.ForeignKey(Session)
#     course_id = models.CharField(max_length=200)
#     downloaded = models.BooleanField(default=False)

#     def __str__(self):
#         return (self.Session, self.course_id, self.downloaded)