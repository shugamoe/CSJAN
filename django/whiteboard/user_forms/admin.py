from django.contrib import admin
from .models import Session, Course


class CourseInline(admin.TabularInline):
    model = Course
    extra = 4


class SessionAdmin(admin.ModelAdmin):
    inlines = [CourseInline]             # quarter and year might not work.  
    list_display = ('cnet_id', 'date', 'quarter', 'year')
    list_filter = ['date']
    # search_fields = ['username']



admin.site.register(Session, SessionAdmin)
# Register your models here.
