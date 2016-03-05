from django.contrib import admin
from .models import Session, Course, Student, Instructor, Assistant, File


class CourseInline(admin.TabularInline):
    model = Course
    extra = 4


class SessionAdmin(admin.ModelAdmin):
    # inlines = [CourseInline]             # quarter and year might not work.  
    list_display = ('cnet_id', 'date', 'quarter', 'year')
    list_filter = ['date']
    # search_fields = ['username']


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'downloaded')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name')

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name')

class AssistantAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name')

class FileAdmin(admin.ModelAdmin):
    list_display = ('path', 'owner', 'course')


# Register your models here.
admin.site.register(File, FileAdmin)
admin.site.register(Assistant, AssistantAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)