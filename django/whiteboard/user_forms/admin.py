from django.contrib import admin
from .models import Session, Class


class ClassInline(admin.TabularInline):
    model = Class
    extra = 4


class SessionAdmin(admin.ModelAdmin):
    inlines = [ClassInline]             # quarter and year might not work.  
    list_display = ('cnet_id', 'date', 'quarter', 'year')
    list_filter = ['date']
    # search_fields = ['username']



admin.site.register(Session, SessionAdmin)
# Register your models here.
