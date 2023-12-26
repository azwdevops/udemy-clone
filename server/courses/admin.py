from django.contrib import admin, sites
from django.contrib.admin import ModelAdmin, register

from .models import Sector, Course, Episode, Comment, CourseSection


admin.site.register(CourseSection)
admin.site.register(Episode)
admin.site.register(Comment)


@register(Sector)
class SectorAdmin(ModelAdmin):
    list_display = ['sector_uuid', ]


@register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ['course_uuid', ]
