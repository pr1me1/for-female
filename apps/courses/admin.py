from django.contrib import admin

from apps.courses.models import Course, Category, Webinar, Module, Lesson, Comment

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Webinar)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Comment)
