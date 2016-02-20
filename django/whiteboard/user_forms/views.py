from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.utils import timezone
from .forms import UserForm
from .models import SessionForm, CourseForm, Session, Course
# Create your views here.

TEST_COURSES = ['STAT 244', 'ENGL 169']


def get_info(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session_object = form.save()
            # Insert code here to interact with crawlers and add session info
            # to the database.
            courses = dummy_crawler(form.cleaned_data, session_object)
            print(courses, session_object.id)
            return HttpResponseRedirect(reverse('select_downloads', \
                                                        args=(session_object.id,)))
        else:
            form = SessionForm()
            return render(request, 'user_forms/start.html', {'form': form})
    else:
        form = SessionForm()

    return render(request, 'user_forms/start.html', {'form': form})
    

def select_downloads(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    print(session.cnet_id, 'the current cnet id')
    print(session.course_set.all(), 'the course selection')
    courses = session.course_set.all()
    if request.method == 'POST':


        # We obtain a list of the 
        courses = get_courses(request)
        for course in courses:
            course_model = session.course_set.get(course_id=course)
            course_model.downloaded=True
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
        pass
    return render(request, 'user_forms/select_downloads.html', \
                                                {'courses': courses})


def post(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    return render(request, 'user_forms/post.html',
                    {'cnet_id': session.cnet_id,
                      'courses': session.course_set.filter(downloaded=True)})

def get_courses(request):
    courses = []
    for i in range(1, len(request.POST) + 1):
        if request.POST.get('course' + str(i)):
            courses.append(request.POST.get('course' + str(i)))

    return courses

def dummy_crawler(cleaned_data, session_object):
    for course in TEST_COURSES:
        session_object.course_set.create(course_id=course, downloaded=False)

    session_object.save()

    # Should call actually web crawler from here to obtain list of courses.  
    # For now we will just use TEST_COURSES.  

    return TEST_COURSES




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