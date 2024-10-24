from django.contrib import admin

from hostel.models import Allotment, Room, Student

# Register your models here.
admin.site.register(Allotment)
admin.site.register(Student)
admin.site.register(Room)