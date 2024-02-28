from django.contrib import admin

# Register your models here.


from .models import Teacher, Student, Test, Question, Choice,OptedChoice,AttemptedTest


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class TestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
    ]
    inlines = [QuestionInline]

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Test, TestAdmin)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(OptedChoice)
admin.site.register(AttemptedTest)
