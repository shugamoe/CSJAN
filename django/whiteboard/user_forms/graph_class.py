from .models import Course, Student

# For test plots
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def graph_class(course_id):
    program_dictionary = {}

    #search through courses in DB for course with ID matching input
    list_of_objects = Course.objects.all()
    for potential_course in list_of_objects:
        db_course_id = potential_course.id
        if db_course_id == course_id:
            plot_course = potential_course
            print("plotting", plot_course)

    #if a course is found, filter students that are in the class.

    list_of_students = Student.objects.filter(courses_in__id=plot_course)
    for student in list_of_students:
    #compile the majors of the students, count them.
        if student.program not in program_dictionary:
            list_of_majors[student.program] = 0
        else:
            list_of_majors[student.program] += 1

    pie_names = []
    pie_nums = []

    for key in program_dictionary:
        pie_names.append(key)
        pie_nums.append(program_dictionary[key])

    plt.figure(figsize=(4, 4))

    plt.pie(pie_nums, labels=pie_names)
    plt.savefig(response)
    plt.close()