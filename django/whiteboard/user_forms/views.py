from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


from .forms import DownloadForm, CourseForm, SessionForm
from .models import Session, Course, Student, Instructor, Assistant, File
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


def get_chalk_info(request):
    '''
    This view is written to obtain user credentials and class filters for 
    Chalk.
    '''
    print('get_chalk_info view')
    print()
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session_object = form.save()
            print(form.cleaned_data)
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
    '''
    This view simply renders the start page, where the user can choose between
    downloading classes from Chalk or viewing stats.
    '''
    print('At start page')
    return render(request, 'user_forms/start.html')

def view_stats(request):
    print('At view stats page')
    return render(request, 'user_forms/view_stats.html')
 
    

def select_downloads(request, session_id, cnet_id):
    '''
    After the user has provided their chalk information, the Chalk crawler 
    retrieves a list of matching courses.  This view brings up a page where
    the user can confirm which classes they want from these matching courses.
    '''
    session = get_object_or_404(Session, pk=session_id)
    
    if request.method == 'POST':
        cnet_pw = request.POST.get('cnet_pw')
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
        courses = Course.objects.filter(sessions__id = session_id)

    return render(request, 'user_forms/select_downloads.html', \
                                                {'courses': courses})


def get_cnet_id(request):
    '''
    This view is called when the user wishes to view their statistics.  The 
    user enters their CNET ID so that the website can retrieve all of the 
    classes associated with that CNET_ID.
    '''
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
    '''
    This view is called after the user has confirmed their choice of classes to
    download.  The view will retrieve all courses downloaded by the user in
    previous sessions as well as display courses selected for download in the
    current session.
    '''
    session = get_object_or_404(Session, pk=session_id)
    all_courses = Course.objects.filter(sessions__cnet_id = session.cnet_id)\
    .filter(downloaded=True).distinct()
    return render(request, 'user_forms/post.html',
                    {'cnet_id': session.cnet_id,
                      'courses': session.course_set.filter(downloaded=True),
                      'all_courses': all_courses})


def dummy_crawler(cleaned_data, session_object):
    '''
    Will function as the connector to Andy and Bonar's crawlers.
    '''

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
                                downloaded = False)
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


class CourseList(ListView):
    model = Course
    context_object_name = 'course_list'

    def get_queryset(self):
        cnet_id = self.kwargs['cnet_id']
        return Course.objects.filter(student__cnet_id=cnet_id)\
             .order_by('dept')


    def get_context_data(self, *args, **kwargs):
        context = super(CourseList, self).get_context_data(*args, **kwargs)
        # I also want to pass the cnet_id and not just use it to filter 
        # for courses.
        cnet_id = self.kwargs['cnet_id']
        context['cnet_id'] = cnet_id
        context['student_id'] = Student.objects.get(cnet_id = cnet_id).id
        course_ids = get_courses_get(self.request)
        course_ids = '/'.join(course_ids)
        context['course_ids'] = course_ids
        return context 

class CourseDetail(DetailView):
    model = Course
    pk_url_kwarg = 'course_id'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseDetail, self).get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        context['students'] = Student.objects.filter(courses_in__id = course_id
        )
        context['instructors'] = Instructor.objects.filter(courses_taught__id = 
        course_id)
        context['assistants'] = Assistant.objects.filter(courses_taught__id = 
        course_id)


        # This will retrieve the user's files.
        context['files'] = File.objects.filter(owner__cnet_id = 
        self.kwargs['cnet_id'])

        return context

class StudentDetail(DetailView):
    model = Student
    pk_url_kwarg = 'student_id'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        student_id = self.kwargs['student_id']
        # Call the base implementation first to get a context
        context = super(StudentDetail, self).get_context_data(**kwargs)
        context['courses_in'] = Course.objects.filter(student__id = student_id)
            
        context['cnet_id'] = Student.objects.get(id = student_id).cnet_id


        course_ids = get_courses_get(self.request)
        course_ids = '/'.join(course_ids)
        context['course_ids'] = course_ids
        return context


def get_courses_post(request):
    '''
    This function is used to extract courses selected from a dynamic form 
    populated with potential classes the user will want to download.
    '''
    courses = []
    for i in range(1, len(request.POST) + 1):
        if request.POST.get('course' + str(i)):
            courses.append(request.POST.get('course' + str(i)))

    return courses

def get_courses_get(request):
    '''
    This function is used to extract courses from a dynamic form populated with
    the classes the user wants to view demographic information about.
    '''
    courses = []
    for i in range(1, len(request.GET) + 1):
        if request.GET.get('course' + str(i)):
            courses.append(request.GET.get('course' + str(i)))
    print('get courses are:', courses)
    return courses




from django.db.models.fields.related import ManyToManyField

def to_dict(instance, ignore_m2m = False):
    '''
    This function is able to turn model instances into an easier form to digest
    for any plotting that might be done.
    '''
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField) and (not ignore_m2m):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list(\
                    'pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data


def student_classes_plot(request, cnet_id, course_ids):
    '''
    This plot will display information about all the classes the Student is 
    included in on Whiteboard.  ALternatively, if the user selects only certain
    classes that the student is in
    '''
    test_names = ['Stud_cls_plt', 'CLASS 2', cnet_id]
    test_nums = [100, 50, 100]

    # If we recieve course_ids, that means that the user has hand selected
    # the classes they want to retrieve information about.  Thus, the plot 
    # presented will only attain information for those selected courses.  
    # (Still needs to be fully implemented)
    if course_ids != 'No_courses_selected':
        course_ids = course_ids.split('/')
        course_ids = [int(course_id) for course_id in course_ids]
        test_names[0] = 'Override CNET_ID'
    else:
        courses = Course.objects.filter(student__cnet_id = cnet_id)
    
    # print('demographics received user courses!!!', courses)
    response = HttpResponse(content_type='image/png')
    plt.figure(figsize=(6, 6))



    plt.pie(test_nums, labels=test_names)
    plt.savefig(response)
    plt.close()

    return response


def single_class_plot(request, course_id):
    '''
    This plot will display information pertaining to a single class.
    '''


    response = HttpResponse(content_type='image/png')

    plt.figure(figsize=(4, 4))

    test_names = ['MAJOR 1', '1_cls_plt', 'course id is: ' + str(course_id)]
    test_nums = [40, 50, 100]

    plt.pie(test_nums, labels=test_names)
    plt.savefig(response)
    plt.close()

    return response