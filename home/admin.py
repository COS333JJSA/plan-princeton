from django.contrib import admin

# Register your models here.
from .models import Req_List, Contact, URL, Department, Concentration, Professor, Listing, Class, Course, Area, Semester, User, SavedCourse, Plan

admin.site.register(Req_List)
admin.site.register(Concentration)
admin.site.register(Contact)
admin.site.register(URL)
admin.site.register(Department)
admin.site.register(Professor)
admin.site.register(Listing)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(Area)
admin.site.register(Semester)
admin.site.register(User)
admin.site.register(SavedCourse)
admin.site.register(Plan)