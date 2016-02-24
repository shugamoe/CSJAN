from django.contrib import admin
from .models import Session, Course, Student


class CourseInline(admin.TabularInline):
    model = Course
    extra = 4


class SessionAdmin(admin.ModelAdmin):
    # inlines = [CourseInline]             # quarter and year might not work.  
    list_display = ('cnet_id', 'date', 'quarter', 'year')
    list_filter = ['date']
    # search_fields = ['username']


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'downloaded')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('cnet_id', 'last_name', 'first_name')



admin.site.register(Session, SessionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
# Register your models here.
