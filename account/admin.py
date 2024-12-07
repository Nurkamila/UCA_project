from django.contrib import admin
from .models import User, Region, School


# Register your models here.
admin.site.register(User)
admin.site.register(Region)
# admin.site.register(School)


class SchoolAdmin(admin.ModelAdmin):
    exclude = ('code',) 


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'code', 'get_director')
    search_fields = ('name', 'region__name')