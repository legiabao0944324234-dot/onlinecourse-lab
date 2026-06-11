from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Course, Lesson, Question, Choice, Submission, Enrollment


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2
    show_change_link = True


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'lesson', 'grade']
    list_filter = ['lesson__course']
    search_fields = ['question_text']


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title']


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)
