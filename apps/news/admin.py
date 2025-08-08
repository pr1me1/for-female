from django.contrib import admin

from apps.news.models import Submission, Post, Event, Survey, Question, QuestionOption

admin.site.register(Submission)
admin.site.register(Post)
admin.site.register(Event)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(QuestionOption)
