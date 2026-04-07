from django.contrib import admin
from .models import *
from student.models import Teacher
# Register your models here.
admin.site.register(Notification)
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(FeeCollection)
admin.site.register(Expense)
admin.site.register(Salary)
admin.site.register(Holiday)
admin.site.register(FeeStructure)
admin.site.register(Exam)
admin.site.register(Event)
admin.site.register(TimeTableEntry)
admin.site.register(LibraryBook)
admin.site.register(SportsActivity)
admin.site.register(HostelRecord)
admin.site.register(TransportRoute)
