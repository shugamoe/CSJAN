from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


from .forms import DownloadForm, CourseForm, SessionForm
from .models import Session, Course, Student, Instructor, Assistant
from django.views.generic import ListView, DetailView


import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

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
                # dl_all_courses(form.cleaned_data)
                url = reverse('post', kwargs = 
                    {'session_id': session_object.id})
            else:

                # Replace with get_prelim_courses when crawlers are integrated.
                courses_to_confirm = dummy_crawler(form.cleaned_data, 
                    session_object)
                # print('cnet id {}'.format(form.cleaned_data['cnet_id']))
                url = reverse('select_downloads', kwargs=
                    {'session_id': session_object.id, 
                    'cnet_id': form.cleaned_data['cnet_id']})
            return HttpResponseRedirect(url)
        else:
            print('form not valid')
            form = SessionForm()
    else:
        form = SessionForm()

    return render(request, 'user_forms/dl_query.html', {'form': form})


def start(request):
    print('At start page')
    return render(request, 'user_forms/start.html')

def view_stats(request):
    print('At view stats page')
    return render(request, 'user_forms/view_stats.html')
 
    

def select_downloads(request, session_id, cnet_id):
    print('select downloads view')
    print()
    print(session_id)
    session = get_object_or_404(Session, pk=session_id)
    
    if request.method == 'POST':

        # cnet_pw = request.POST.get('cnet_pw')

        courses = get_courses_post(request)

        print('courses should be here: ', courses)
        if not courses:
            return render(request, 'user_forms/select_downloads.html', \
                            {'courses': session.course_set.all(),
                             'error_message': "You didn't choose any courses"})
        else:
            print('courses has stuff in it')
            for course in courses:
                course_model = Course.objects.get(name=course)
                course_model.downloaded = True
                course_model.save()

            # dl_specific_courses(courses, (cnet_id, cnet_pw))

            return HttpResponseRedirect(reverse('post', \
                                            args=(session.id,)))
    else:
        print('Session ID: {}'.format(session_id))
        courses = Course.objects.filter(sessions__id = session_id)
        print('courses should be here', courses)
    return render(request, 'user_forms/select_downloads.html', \
                                                {'courses': courses})


def get_cnet_id(request):
    print('getting cnet id')
    if request.method == 'POST':
        cnet_id = request.POST.get('cnet_id')
        print('CNET ID is {}'.format(cnet_id))
        if not cnet_id:
            return render(request, 'user_forms/get_cnet_id.html', \
            {'error_message': "You didn't enter a CNET ID"})
        else:
            return HttpResponseRedirect(reverse('view_courses', kwargs = 
                {'cnet_id': cnet_id}))
    else:
        return render(request, 'user_forms/get_cnet_id.html')


def post(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    all_courses = Course.objects.filter(sessions__cnet_id = session.cnet_id).distinct()
    return render(request, 'user_forms/post.html',
                    {'cnet_id': session.cnet_id,
                      'courses': session.course_set.filter(downloaded=True),
                      'all_courses': all_courses})


def dummy_crawler(cleaned_data, session_object):
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
        num_results = Course.objects.filter(name = course).count()
        if num_results == 0:
        # {TO DO} Add in more fields 
            course_object = Course(name = course, 
                                downloaded = dled_default)
            course_object.save()
        else:
            course_object = Course.objects.get(name = course)

        course_object.sessions.add(session_object)

    # Should call actually web crawler from here to obtain list of courses.  
    # For now we will just use TEST_COURSES.  

    return test_courses

def get_prelim_courses(credens_and_filters, sessions_object):
    '''
    This function calls the Chalk Crawler and asks it for a preliminary set of 
    courses for the user to confirm at the select_downloads section.
    '''

    # c_crawler.find_matching is a dummy function, replace with the 
    # actual function later.
    course_dicts = c_crawler.find_matching(credens_and_filters)

    prelim_courses = []

    for course_dict in course_dicts:
        course_name = course_dict['name']
        prelim_courses.append(course_name)

        num_results = Course.objects.filter(name = course_name)
        if num_results == 0:
            course_object = Course(**course_dict)
            course_object.save()
        else:
            course_object = Course.objects.get(name = course_name)

    return prelim_courses


def dl_specific_courses(course_list, credentials_tuple):
    '''
    This function will call the Chalk Crawler and Directory Crawler after the
    user has specified which specific courses they would like to download
    '''
    # Pass the course list to and credentials to Chalk crawler, then have it
    # return File dicts to make file models, and lists of teacher, student, and
    # TA info for the Directory crawler.
    #
    # Take the lists, and send them to the directory crawler, which will return
    # dicts to make Student, teacher, and TA models.  Do not make duplicates
    # of the Student, teacher, and TA models.
    # 
    # c_crawler.dl_
    # File models can be duplicated across cnet_ids but not within cnet_ids.
    #
    # 
    # Remember after making each model instance to add the correct manytomany
    # field or manytoone field.  (TA's, Students, and Instructors all have
    # to have courses added to them.  File models have a Student foreignkey 
    # "owner".)

    pass

def dl_all_courses(cleaned_data):
    '''
    This function will call the Chalk Crawler and Directory Crawler if the user
    desires to download all their courses.
    '''
    # Pass the cleaned_data dict


    pass






class CourseList(ListView):
    model = Course
    context_object_name = 'course_list'

    def get_queryset(self):
        self.cnet_id = self.kwargs['cnet_id']
        return Course.objects.filter(student__cnet_id=self.cnet_id)\
             .order_by('dept')


    def get_context_data(self, *args, **kwargs):
        context = super(CourseList, self).get_context_data(*args, **kwargs)
        # I also want to pass the cnet_id and not just use it to filter 
        # for courses.
        context['cnet_id'] = self.kwargs['cnet_id']
        get = get_courses_get(self.request)
        context['form_processed'] = get
        return context 

class CourseDetail(DetailView):
    model = Course
    pk_url_kwarg = 'course_id'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['students'] = Student.objects.filter(courses_in__id = 
        self.kwargs['course_id'])
        return context

class StudentDetail(DetailView):
    model = Student
    pk_url_kwarg = 'student_id'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StudentDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['courses_in'] = Course.objects.filter(student__id = 
            self.kwargs['student_id'])
        return context


def get_courses_post(request):
    courses = []
    for i in range(1, len(request.POST) + 1):
        if request.POST.get('course' + str(i)):
            courses.append(request.POST.get('course' + str(i)))

    return courses

def get_courses_get(request):
    courses = []
    for i in range(1, len(request.GET) + 1):
        if request.GET.get('course' + str(i)):
            courses.append(request.GET.get('course' + str(i)))
    print('get courses are:', courses)
    return courses




from django.db.models.fields.related import ManyToManyField

def to_dict(instance):
    '''
    This function is able to turn model instances into an easier form to digest
    for any plotting that might be done.
    '''
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list(\
                    'pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data


def user_classes_plot(request, cnet_id):
    '''
    This plot will display information about all the classes the user has 
    uploaded to Whiteboard.
    '''
    # print('demographics received user courses!!!', courses)
    response = HttpResponse(content_type='image/png')
    plt.figure(figsize=(4, 4))

    test_names = ['CLASS 1', 'CLASS 2', cnet_id]
    test_nums = [40, 50, 100]

    plt.pie(test_nums, labels=test_names)
    plt.savefig(response)
    plt.close()

    return response