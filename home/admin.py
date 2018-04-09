from django.contrib import admin

# Register your models here.
from .models import Req_List, Requirement, Contact, URL, Department, Professor, Listing, Class, Course, Area

admin.site.register(Req_List)
admin.site.register(Requirement)
admin.site.register(Contact)
admin.site.register(URL)
admin.site.register(Department)
admin.site.register(Professor)
admin.site.register(Listing)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(Area)