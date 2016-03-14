from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


<<<<<<< HEAD
from .forms import SessionForm, FilterMajorForm
=======
from .forms import SessionForm, FilterMajorForm, ClassFilesSearchForm, \
SelectCoursesForm
>>>>>>> f384d0a7c655203404acd4b251544e64a9e05893
from .models import Session, Course, Student, Instructor, Assistant, File
from django.views.generic import ListView, DetailView

# Special mpl imports from Django workshop code.
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import random
import re
from .chalk_crawler import get_courses, dl_specific_courses 
from .directory_crawler_edit import crawl_multiple_classes as get_demog_dicts
from .graph_class import graph_class 

from django.core.management import call_command
from haystack.generic_views import SearchView
from haystack.forms import SearchForm
import subprocess
import os
from django.core.exceptions import ObjectDoesNotExist

# import folders 
# Create your views here.

TEST_COURSES_0 = ['STAT 244', 'ENGL 169']
TEST_COURSES_1 = ['CMSC 122', 'MATH 195']
TEST_COURSES_2 = ['PORK 101', 'BEEF 504']


def get_chalk_info(request):
    '''
    This view deploys to obtain user credentials and class filters for 
    the Chalk Crawler to obtain a preliminary list of classes.

    Inputs:
        request: a REQUEST object.

    Ouputs:
        Renders dl_query.html if an invalid POST request or no POST request.  
        Otherwise if there is a valid POST request it returns a response 
        redirect to 'select_downloads' url.
    '''
    print('Obtaining Chalk Credentials and Filters')
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session_object = form.save()
            # Replace with chalk_crawler.get_prelim(form.cleaned_data) when 
            # crawlers are integrated.
            courses_to_confirm = get_courses(form.cleaned_data)
            print(courses_to_confirm, 'COURSES TO CONFIRM')
            if courses_to_confirm == None: # Invalid CNET ID OR PW
                error_message = 'Invalid CNET ID or Password'
            else:
                # Clever trick I found on StackExchange to send information like
                # pk's, and other information through the url.
                # This also appears elsewhere.   
                # http://stackoverflow.com/questions/249110/django-arbitrary-number-of-unnamed-urls-py-parameters
                courses_to_confirm = '***'.join(courses_to_confirm)
                url = reverse('select_downloads', kwargs = \
                    {'session_id': session_object.id, 
                    'cnet_id': form.cleaned_data['cnet_id'],
                    'courses_to_confirm': courses_to_confirm})
            return HttpResponseRedirect(url)     
        else:
            error_message = 'Remember to enter a CNET ID and Password'
    else:
        error_message = None

    form = SessionForm()

    return render(request, 'user_forms/dl_query.html', {'form': form})


def start(request):
    '''
    This view simply renders the start page, where the user can choose between
    downloading classes from Chalk or viewing stats.

    Inputs:
        request: a REQUEST object.

    Outputs:
        Renders start.html.
    '''
    print('Start page')
    return render(request, 'user_forms/start.html')


def browse_classes(request):
    '''
    This view simply renders the start page, where the user can choose between
    downloading classes from Chalk or viewing stats.

    Inputs:
        request: a REQUEST object.

    Outputs:
        Renders browse_classes.html.
    '''
    print('At view stats page')
    return render(request, 'user_forms/browse_classes.html')
 
    

def select_downloads(request, session_id, cnet_id, courses_to_confirm):
    '''
    After the user has provided their chalk information, the Chalk crawler 
    retrieves a list of matching courses.  This view brings up a page where
    the user can confirm which classes they want from these matching courses and
    reenter their CNET password to begin collecting demographic information and
    downloading files.

    Inputs:
        request: a REQUEST object 
        session_id: the unique session id (pk) [int] 
        cnet_id: the current user's CNET ID [str]
        courses_to_confirm: a concatenated string of unique course names for the 
                            viewer to select
    Outputs:
        Renders select_downloads.html to begin with.  If there is an invalid 
        post request the same render is returned with an error message.  A
        successful POST request this view redirects to 'post' url.
    '''
    print('Select downloads (classes to download)')
    session = get_object_or_404(Session, pk=session_id)
    courses = courses_to_confirm.split('***') # Unpack course names
    error_message = None

    if request.method == 'POST':
        form = SelectCoursesForm(request.POST, **{'course_list': courses })
        if form.is_valid():
            confirmed_courses = form.cleaned_data['course_choices']
            cnet_pw = form.cleaned_data['cnet_pw']

            crawlers_link(request, confirmed_courses, cnet_id, cnet_pw, session)
            return HttpResponseRedirect(reverse('post', \
                                            args = (session.id,)))
        else:
            error_message = 'Remember to enter your CNET ID and to select one'\
            'or more courses'

    form = SelectCoursesForm(**{'course_list': 
            courses})  

    return render(request, 'user_forms/select_downloads.html', \
                                                {'courses': courses,
                                                'form': form,
                                                'error_message': error_message})


def get_cnet_id(request):
    '''
    This view is called when the user (with an unknown CNET ID) wishes to browse
    their classes.  The user enters their CNET ID so that the website can 
    retrieve all of the classes associated with that CNET_ID.

    Inputs:
        request: a REQUEST object
    Outputs:
        renders get_cnet_id.html to start (with an error message) if the user 
        submits with no CNET ID.  Otherwise if a CNET_ID is entered it redirects
        to 'view_courses' url.
    '''
    print('Get CNET ID')
    if request.method == 'POST':
        cnet_id = request.POST.get('cnet_id')
        if not cnet_id: # User didn't enter a CNET ID
            return render(request, 'user_forms/get_cnet_id.html', \
            {'error_message': "You didn't enter a CNET ID"})
        else:
            # Quickly check to see if a student with that CNET ID exists.
            test = Student.objects.filter(cnet_id = cnet_id).count()
            print('test', test)
            if test == 0: # Return error if no info for CNET ID exists.
                return render(request, 'user_forms/get_cnet_id.html',
                    {'does_not_exist': True, 'wrong_cnet': cnet_id})
            
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

    Inputs:
        request: a REQUEST object
        session_id: the unique session id (pk) [int]
    Outputs:

    '''
    session = get_object_or_404(Session, pk=session_id)

    prev_courses = Course.objects.filter(sessions__date__lt = 
        session.date).filter(sessions__cnet_id = session.cnet_id).distinct()
    
    if len(prev_courses) > 0:
        session.repeat_user = True
        session.save()

    return render(request, 'user_forms/post.html',
                    {'courses': session.course_set.all(),
                      'prev_courses': prev_courses,
                      'repeat_user': session.repeat_user,
                      'cnet_id': session.cnet_id})


def dummy_crawler(cleaned_data, session_object):
    '''
    Dummy function while crawlers are being completed.
    '''
    # These lines use some simple random stuff to "select" classes.  
    num = random.randrange(0,3)
    if num == 0:
        test_courses = TEST_COURSES_0
    elif num == 1:
        test_courses = TEST_COURSES_1
    elif num == 2: 
        test_courses = TEST_COURSES_2

    return test_courses


def crawlers_link(request, course_name_list, cnet_id, cnet_pw, session_object):
    '''
    This function will call the Chalk Crawler and Directory Crawler after the
    user has specified which specific courses they would like to download

    Inputs:
        course_name_list: a list of unique course names to gather info on.
        cnet_id: the user's CNET ID [str]
        cnet_pw: the user's CNET Password [str]
        session_object: an instance of the Session model, the user's current
                        session
    Returns:
        None
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

    # Utilize the chalk crawler to  obtain demog_names: a list of first and
    # last names of instructors, TAs, and students (may not exist if the class
    # is too far in the past).  Chalk crawler also obtains file_dicts for each
    # file downloaded.  These dicts are used to update or create instances 
    # of the file model in the database (to allow for search functionality and
    # opening of the file from the database.)
    demog_names, file_dicts = dl_specific_courses(course_name_list, cnet_id,
     cnet_pw, session_object.people_only)

    if (demog_names == None) and (file_dicts == None): # Invalid credentials
        render(request, 'user_forms/select_downloads.html', \
                                                {'courses': course_name_list,
                                                'error_message': 'Invalid' 
                                                ' CNET ID \or Password'})
    demog_dicts = get_demog_dicts(demog_names, cnet_id, cnet_pw)

    # Depending on whether the demog_dicts correspond to instructors, TAs, or
    # students, we call the a_or_u_people function with the appropriate model
    # type of Instructor, Assistant, and Student respectively.
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

    # Add or update instances of the File model in the database from information
    # returned by the Chalk Crawler.
    a_or_u_files(file_dicts)


    # This command ensures that the search indexes for Haystack are updated.
    # (So you can search the latest files.)
<<<<<<< HEAD
=======
    # http://stackoverflow.com/questions/6250970/run-custom-admin-command-from-view
>>>>>>> f384d0a7c655203404acd4b251544e64a9e05893
    call_command('update_index')

    return None


def a_or_u_files(file_dicts):
    '''
    This function takes in a list of file_dicts, where each element is a 
    a dictionary that can be directly converted to an instance of the File 
    class.

    This function checks the information of each dict to see whether the 
    database already has an instance of that file and updates the information 
    for that instance if it already exists.

    Inputs:
        file_dicts: dictionaries that can be used either to update or create 
                    instances of File models.
    '''
    for file_dict in file_dicts:
        course_id = Course.objects.get(name = file_dict.pop('course')).id

        # Foreign key.
        file_dict['course_id'] = course_id

        # The search engine library I have has trouble narrowing down querysets
        # using foreign keys so I simply made an attribute that records the same
        # information as the foreignkey for later use.  
        # (See SearchClassFilesView)
        file_dict['classpk'] = str(course_id)

        # Add/Update idea from http://stackoverflow.com/questions/14115318/create-django-model-or-update-if-exists
        # Also used in a_or_u_people()
        existing_instance, created = File.objects.get_or_create(path = 
            file_dict['path'], defaults = file_dict)
        if not created:
            for attr, value in file_dict.items():
                setattr(existing_instance, attr, value)
            existing_instance.save

    return None


def a_or_u_people(people_dicts, model_used, course_name):
    '''
<<<<<<< HEAD
    This function takes in a list of dictionaries that can be used to create
    or update instances of the model_used.  The course_name is used to link 
    these instances to the course that they are a part of.
=======
    This function takes in a list of people_dicts, where each element is a 
    a dictionary that can be directly converted to an instance of the model_used
    class.

    This function checks the information of each dict to see whether the 
    database already has an instance of that file and updates the information 
    for that instance if it already exists.

    Inputs:
        people_dicts: dictionaries that can be used either to update or create 
                      instances of model_used.
        model_used: The model to be used in the function.  Either Instructor,
                    Assistant, or Student.
        course_name: The name of the course that the people are in. [str]

    Returns:
        None
>>>>>>> f384d0a7c655203404acd4b251544e64a9e05893
    '''
    course_object = Course.objects.get(name = course_name)

    for ppl_dict in people_dicts:
        existing_instance, created = model_used.objects.get_or_create(email = 
            ppl_dict['email'], defaults = ppl_dict)
        if not created:
            for attr, value in ppl_dict.items():
                setattr(existing_instance, attr, value)
            existing_instance.save
            existing_instance.courses_in.add(course_object)
        else:
            existing_instance = model_used.objects.get(email = 
                ppl_dict['email'])
            existing_instance.save
            existing_instance.courses_in.add(course_object)

    return model_used.objects.all()


class CourseList(ListView):
    '''
    A generic ListView for the user to view all courses that they are in.
    '''
    model = Course
    context_object_name = 'course_list'

    def get_queryset(self):
        cnet_id = self.kwargs['cnet_id']

        # Only want to view courses that the user is in.
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
    '''
    A generic DetailView for the user to view a specific course
    '''
    model = Course
    pk_url_kwarg = 'course_id'
    context_object_name = 'course'


    def get_context_data(self, **kwargs):
        context = super(CourseDetail, self).get_context_data(**kwargs)
        course_id = self.kwargs['course_id']


        # Retrieve a list of students in the class for the template
        context['students'] = Student.objects.filter(courses_in__id = course_id
        ).order_by('first_name')


        # See what majors those students have so we can create a form to let
        # the user filter by major
        major_tuples = Student.objects.filter(courses_in__id = course_id)\
        .order_by().values_list('program').distinct()

        # To a bit of list comprehension to give it to the form in a nicer 
        # format.
        majors_list = [x[0] for x in major_tuples]
        context['major_filter_form'] = FilterMajorForm(**{'majors_list': 
            majors_list})

        # Handle the filter by major form.
        if self.request.method == 'GET':
<<<<<<< HEAD
            form = FilterMajorForm(self.request.GET, **{'majors_list': 
                majors_list})
=======
            form = FilterMajorForm(self.request.GET, 
                **{'majors_list': majors_list})
>>>>>>> f384d0a7c655203404acd4b251544e64a9e05893
            if form.is_valid():
                majors = form.cleaned_data['major_filters']
            else: 
                context['form_error'] = 'You must select one or more majors!'
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

<<<<<<< HEAD
        # This will retrieve the user's files.
        context['files'] = File.objects.filter(course__id = course_id)
        context['cnet_id'] = self.kwargs['cnet_id']
=======
        # Retrieve all files for this class.
        context['files'] = File.objects.filter(course__id = course_id)
>>>>>>> f384d0a7c655203404acd4b251544e64a9e05893

        return context


class InstructorDetail(DetailView):
    '''
    A generic DetailView for the user to view an Instructor's information.
    '''
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
    '''
    A generic DetailView for the user to view a TA's information
    '''
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
    '''
    A generic DetailView for the user to view a Student's information.
    '''
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
        print('course ids are', course_ids)
        return context

class SearchClassFilesView(SearchView):
    '''
    This is a SearchView to enable the user to search the files for a specific 
    class.
    '''
    template_name = 'user_forms/search_class_files.html'
    form_class = SearchForm


    def get_queryset(self):
        queryset = super(SearchClassFilesView, self).get_queryset()
<<<<<<< HEAD
        print('initial queryset has', queryset.count(), 'results')
        cnet_id = self.kwargs['cnet_id']
        course_id = self.kwargs['course_id']
        # further filter queryset based on some set of criteria

        self.sqs = queryset.filter(course__id = course_id)
        print(self.sqs.count(), '(num_results)')
        return self.sqs
=======
        course_id = self.kwargs['course_id']

        # Ensure that we are only searching through files pertaining to a 
        # certain course.
        sqs = queryset.filter(classpk = str(course_id))
        return sqs
>>>>>>> f384d0a7c655203404acd4b251544e64a9e05893

    def get_context_data(self, *args, **kwargs):
        context = super(SearchClassFilesView, self).get_context_data(*args, 
            **kwargs)
        # do something
        course_id = self.kwargs['course_id']
        context['course_id'] = course_id
        context['course_name'] = Course.objects.get(id = course_id).name
        return context

<<<<<<< HEAD

def get_courses_post(request):
=======
def view_file(request, file_id, course_id, query):
>>>>>>> f384d0a7c655203404acd4b251544e64a9e05893
    '''
    This view deploys when the user views a file.  The webpage rendered displays
    information about the file.  If the user is viewing the file from the search
    interface then information about the query is also displayed.

    Inputs:
        request: a REQUEST object
        file_id: The unique file id (pk)
        query: a string of the query the user has entered.

    Outputs:
        Renders view_file.html with appropriate information and opens
        the file for the user in a separate window.
    '''
    course_name = Course.objects.get(id = course_id)
    file_object = File.objects.get(id = file_id)
    file_name = file_object.file_name()
    file_path = file_object.path
    file_heading = file_object.heading
    file_description = file_object.description

    # Open the file the user is viewing.
    os.system('gnome-open' + ' ' + "'" + str(file_path) + "'")

    if query == 'NOT FROM SEARCH':
        query = None

    return render(request, 'user_forms/view_file.html', {'course_name': 
        course_name, 'file_name':file_name, 'heading': file_heading,
         'description': file_description, 'query': query})
    

def get_courses_get(request):
    '''
    This function is used to extract courses from a dynamic form populated with
    the classes the user wants to view demographic information about.
    '''
    courses = []
    for i in range(1, len(request.GET) + 1):
        if request.GET.get('course' + str(i)):
            courses.append(request.GET.get('course' + str(i)))
    return courses


def student_classes_plot(request, cnet_id, course_ids):
    '''
    This function will return a plot containing information about all the 
    classes the Student is included in on Whiteboard.  Alternatively, if the
    user selects only certain classes that the student is in, this function
    will return a plot containing information about those specific classes only.

    [Modified from Gustav's Django workshop code.]

    Inputs:
        request: a REQUEST object
        cnet_id: the user's CNET ID [str]
        course_ids: a concatenated string of course id numbers.

    Ouputs:
        response: an image/png HttpResponse
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
        # If the student has selected  one class, then we # simply return the 
        # single_class_plot.
        if len(course_ids) == 1:
            return single_class_plot(request, course_ids[0])
        test_names[0] = 'Override CNET_ID'
    else:
        courses = Course.objects.filter(student__cnet_id = cnet_id)
        if len(courses) == 1:
            return single_class_plot(request, courses[0].id)
    
    response = HttpResponse(content_type='image/png')
    plt.figure(figsize=(6, 6))

    plt.pie(test_nums, labels=test_names)
    plt.savefig(response)
    plt.close()

    return response


def single_class_plot(request, course_id):
    '''
    This function will return a pie plot containing the major breakdown within
    each class.

    [Modified from Gustav's Django workshop code.]

    Inputs:
        request: a REQUEST object
        course_id: the unique id for a course (pk) [str]

    Outputs:
        response: an image/png HttpResponse
    '''
    response = HttpResponse(content_type='image/png')

    plt.figure(figsize=(6, 6))

    program_dictionary = {}

    # If a course is found, filter students that are in the class.
    list_of_students = Student.objects.filter(courses_in__id=course_id)
    for student in list_of_students:
    # Compile the majors of the students, count them.
        if student.program not in program_dictionary:
            program_dictionary[student.program] = 0
        else:
            program_dictionary[student.program] += 1

    pie_names = []
    pie_nums = []
    formatted_dictionary = {"Other": 0}

    for key in program_dictionary:
        value = program_dictionary[key]
        if value >= 4:
            formatted_dictionary[key] = value
        else:
            formatted_dictionary["Other"] += value

    assert len(formatted_dictionary.keys()) >= 2

    for key in formatted_dictionary:
        pie_names.append(key)
        pie_nums.append(formatted_dictionary[key])

    plt.pie(pie_nums, labels=pie_names)
    plt.savefig(response)
    plt.close()

    return response
