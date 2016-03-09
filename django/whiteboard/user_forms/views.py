from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


from .forms import SessionForm, FilterMajorForm
from .models import Session, Course, Student, Instructor, Assistant, File
from django.views.generic import ListView, DetailView

# For test plots
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import random
import re
from .chalk_crawler import get_courses, dl_specific_courses 
from .directory_crawler import crawl_multiple_classes as get_demog_dicts
from .graph_class import graph_class 


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
            # Replace with chalk_crawler.get_prelim(form.cleaned_data) when 
            # crawlers are integrated.
            courses_to_confirm = get_courses(form.cleaned_data)

            # Clever trick I found on StackExchange to send information like
            # pk's, and other information through the url.
            courses_to_confirm = '***'.join(courses_to_confirm)
            url = reverse('select_downloads', kwargs = \
                {'session_id': session_object.id, 
                'cnet_id': form.cleaned_data['cnet_id'],
                'courses_to_confirm': courses_to_confirm})

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
 
    

def select_downloads(request, session_id, cnet_id, courses_to_confirm):
    '''
    After the user has provided their chalk information, the Chalk crawler 
    retrieves a list of matching courses.  This view brings up a page where
    the user can confirm which classes they want from these matching courses.
    '''
    session = get_object_or_404(Session, pk=session_id)
    
    if request.method == 'POST':
        cnet_pw = request.POST.get('cnet_pw')
        courses = get_courses_post(request)

        if not courses:
            return render(request, 'user_forms/select_downloads.html', \
                            {'courses': session.course_set.all(),
                             'error_message': "You didn't choose any courses"})
        else:

            crawlers_link(courses, cnet_id, cnet_pw, session)

            return HttpResponseRedirect(reverse('post', \
                                            args = (session.id,)))
    else:
        courses = courses_to_confirm.split('***')

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

    prev_user_sessions = Session.objects.filter(date__lt = session.date)\
    .filter(cnet_id = session.cnet_id).count()

    print(session.cnet_id, 'this is the CNET ID of the current user session')
    print(session.date, 'the date!')
    prev_courses = Course.objects.filter(sessions__date__lt = session.date).filter(sessions__cnet_id = session.cnet_id).distinct()
    
    if len(prev_courses) > 0:
        session.repeat_user = True
        session.save()

    return render(request, 'user_forms/post.html',
                    {'courses': session.course_set.all(),
                      'prev_courses': prev_courses,
                      'repeat_user': session.repeat_user,
                      'cnet_id': session.cnet_id})


# sampledate__lt=datetime.date(2011, 1, 31)

def dummy_crawler(cleaned_data, session_object):
    '''
    Will function as the connector to Andy and Bonar's crawlers.
    '''

    # print(cleaned_data['cnet_id'])

    # These lines use some simple random stuff to "select" classes.  
    num = random.randrange(0,3)
    if num == 0:
        test_courses = TEST_COURSES_0
    elif num == 1:
        test_courses = TEST_COURSES_1
    elif num == 2: 
        test_courses = TEST_COURSES_2

    # Should call actually web crawler from here to obtain list of courses.  
    # For now we will just use TEST_COURSES.  

    return test_courses


def crawlers_link(course_name_list, cnet_id, cnet_pw, session_object):
    '''
    This function will call the Chalk Crawler and Directory Crawler after the
    user has specified which specific courses they would like to download
    '''

    year = session_object.year
    quart_pat = r'(?<=\()([A-Z]{1}[a-z]+)'
    dept_pat = r'[A-Z]{4}'

    for course_name in course_name_list:
        # Check if the course already exists, course_name is a unique 
        # identifier in the form DEPT ##### (QUARTER ##) COURSE TITLE.
        # If the course does not exist in the database already, then we add
        # it in.
        num_results = Course.objects.filter(name = course_name).count()
        if num_results == 0:
            dept = re.search(dept_pat, course_name).group()
            quarter = re.search(quart_pat, course_name).group()
            course_dict = {'quarter': quarter, 'year': year, 'dept': dept, 
            'name': course_name}
            course_object = Course(**course_dict)
            course_object.save()
        else:
            course_object = Course.objects.get(name = course_name)
        
        # Either way we track that this course was utilized in the current
        # session by adding the session object to it.
        course_object.sessions.add(session_object)



    demog_names, file_dicts = dl_specific_courses(course_name_list, cnet_id,
     cnet_pw)

    demog_dicts = get_demog_dicts(demog_names, cnet_id, cnet_pw)


    for course in demog_dicts.keys():
        for stud_ta_or_instr in demog_dicts[course].keys():
            if stud_ta_or_instr == 'students':
                a_or_u_people(demog_dicts[course][stud_ta_or_instr], Student,
                    course)
            elif stud_ta_or_instr == 'instructors':
                a_or_u_people(demog_dicts[course][stud_ta_or_instr], 
                    Instructor, course)
            elif stud_ta_or_instr == 'TAs':
                a_or_u_people(demog_dicts[course][stud_ta_or_instr], 
                    Assistant, course)

    a_or_u_files(file_dicts, cnet_id)

    return None


def a_or_u_files(file_dicts, cnet_id):
    '''
    This function takes in a list of file_dicts, where each element is a 
    a dictionary that can be directly converted to an instance of the File 
    class.

    This function checks the information of each dict to see whether the 
    database already has an instance of that 
    '''
    user = Student.objects.get(cnet_id = cnet_id)

    for file_dict in file_dicts:
        course_id = Course.objects.get(name = file_dict.pop('course')).id
        file_dict['course_id'] = course_id
        file_dict['owner_id'] = user.id
        existing_instance, created = File.objects.get_or_create(path = 
            file_dict['path'], defaults = file_dict)
        if not created:
            for attr, value in file_dict.items():
                setattr(existing_instance, attr, value)
            existing_instance.save

    return None


def a_or_u_people(people_dicts, model_used, course_name):
    '''
    '''
    # course_object.sessions.add(session_object)
    course = Course.objects.get(name = course_name)

    for ppl_dict in people_dicts:
        existing_instance, created = model_used.objects.get_or_create(email = 
            ppl_dict['email'], defaults = ppl_dict)
        if not created:
            for attr, value in ppl_dict.items():
                setattr(existing_instance, attr, value)
            existing_instance.save
            existing_instance.courses_in.add(course)
        else:
            existing_instance = model_used.objects.get(email = 
                ppl_dict['email'])
            existing_instance.save
            existing_instance.courses_in.add(course)

    return model_used.objects.all()


class CourseList(ListView):
    model = Course
    context_object_name = 'course_list'

    def get_queryset(self):
        cnet_id = self.kwargs['cnet_id']
        return Course.objects.filter(student__cnet_id = cnet_id)\
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


        # Retrieve a list of students in the class for the template
        context['students'] = Student.objects.filter(courses_in__id = course_id
        ).order_by('program')


        # See what majors those students have so we can create a form to let
        # the user filter by major
        major_tuples = Student.objects.filter(courses_in__id = course_id)\
        .order_by().values_list('program').distinct()

        # To a bit of list comprehension to give it to the form in a nicer 
        # format.
        majors_list = [x[0] for x in major_tuples]
        context['major_filter_form'] = FilterMajorForm(**{'majors_list': 
            majors_list})


        if self.request.method == 'GET':
            form = FilterMajorForm(self.request.GET, **{'majors_list': majors_list})
            if form.is_valid():
                majors = form.cleaned_data['major_filters']
            if majors:
                context['filter_enabled'] = True
                context['students'] = context['students'].filter(program__in = 
                        majors).order_by('program')
            else:
                context['filter_enabled'] = False
        
        context['instructors'] = Instructor.objects.filter(courses_in__id = 
        course_id)
        context['assistants'] = Assistant.objects.filter(courses_in__id = 
        course_id)

        # This will retrieve the user's files.
        context['files'] = File.objects.filter(owner__cnet_id = 
        self.kwargs['cnet_id'])

        return context


class InstructorDetail(DetailView):
    model = Instructor
    pk_url_kwarg = 'instructor_id'
    context_object_name = 'instructor'

    def get_context_data(self, **kwargs):
        instructor_id = self.kwargs['instructor_id']

        context = super(InstructorDetail, self).get_context_data(**kwargs)
        context['courses_in'] = Course.objects.filter(instructor__id = 
            instructor_id)
        context['cnet_id'] = Instructor.objects.get(id = instructor_id).cnet_id
        return context


class AssistantDetail(DetailView):
    model = Assistant
    pk_url_kwarg = 'assistant_id'
    context_object_name = 'assistant'

    def get_context_data(self, **kwargs):
        assistant_id = self.kwargs['assistant_id']

        context = super(AssistantDetail, self).get_context_data(**kwargs)
        context['courses_in'] = Course.objects.filter(assistant__id = 
            assistant_id)
        context['cnet_id'] = Assistant.objects.get(id = assistant_id).cnet_id
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


def single_class_plot(request, course_id, threshold):
    '''
    This plot will display information pertaining to a single class.
    '''

    response = HttpResponse(content_type='image/png')

    plt.figure(figsize=(6, 6))

    program_dictionary = {}

    #if a course is found, filter students that are in the class.
    list_of_students = Student.objects.filter(courses_in__id=course_id)
    for student in list_of_students:
    #compile the majors of the students, count them.
        if student.program not in program_dictionary:
            program_dictionary[student.program] = 0
        else:
            program_dictionary[student.program] += 1

    pie_names = []
    pie_nums = []
    formatted_dictionary = {"Other": 0}

    for key in program_dictionary:
        value = program_dictionary[key]
        if value >= 2:
            formatted_dictionary[key] = value
        else:
            formatted_dictionary["Other"] += value

    for key in formatted_dictionary:
        pie_names.append(key)
        pie_nums.append(program_dictionary[key])

    print('STUFF!!!', pie_nums, pie_names)
    plt.pie(pie_nums, labels=pie_names)
    plt.savefig(response)
    plt.close()

    return response


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











# def scrub_duplicate_ias(course_demos):
#     '''
#     This function takes the raw demographic information from the Chalk crawler
#     which is in the form:

#     [['coursename0', [<list of Instructor Names>], [<list of Assistant names>],
#      [<list of Student Names>]],
#      .
#      .
#      .
#      ]

#     This function checks to see whether or not the database already contains
#     an instance of either the Instructor, Assistant, or Student models that
#     '''
#     for course_demo in demo_info:
#         course_demo[0] = course_name
#         course_demo[1] = instructor_list
#         course_demo[2] = assistant_list
#         course_demo[3] = student_list

#         for i_index, instr in enumerate(instructor_list):
#             last_name, first_name = intr.split(', ')
#             num_results = Instructor.objects.filter(courses_in__name = 
#                 course_name).filter(first_name = first_name).filter(last_name =
#                 last_name).count()
#             if num_results >= 1:
#                 print('Already have instructor {0} {1}'.format(first_name, 
#                     last_name))
#                 instructor_list.pop(i_index)

#         for a_index, assistant in enumerate(assistant_list):
#             last_name, first_name = intr.split(', ')
#             num_results = Assistant.objects.filter(courses_in__name = 
#                 course_name).filter(first_name = first_name).filter(last_name =
#                 last_name).count()
#             if num_results >= 1:
#                 print('Already have assistant {0} {1}'.format(first_name,
#                     last_name))
#                 assistant_list.pop(a_index)

#         for s_index, assistant in enumerate(student_list):
#             last_name, first_name = intr.split(', ')
#             num_results = Assistant.objects.filter(courses_in__name = 
#                 course_name).filter(first_name = first_name).filter(last_name =
#                 last_name).count()
#             if num_results >= 1:
#                 print('Already have student {0} {1}'.format(first_name,
#                     last_name))
#                 student_list.pop(a_index)

#     return None