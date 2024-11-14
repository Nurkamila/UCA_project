from django.contrib import admin
from .models import Subject, StudentProfile, Grade

admin.site.register(Subject)
admin.site.register(StudentProfile)
admin.site.register(Grade)