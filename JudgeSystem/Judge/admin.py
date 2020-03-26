from django.contrib import admin
from .models import User, Problem, Problem_table, Submission, Exam_user, Exam_problem, Exam

# Register your models here.

admin.site.site_header = 'Judge System Administration'

admin.site.register(User)

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
	list_display = ('title',)

@admin.register(Problem_table)
class Problem_tableAdmin(admin.ModelAdmin):
	list_display = ('name',)

admin.site.register(Submission)

@admin.register(Exam_user)
class Exam_userAdmin(admin.ModelAdmin):
	list_display = ('exam_id', 'user_id')

@admin.register(Exam_problem)
class Exam_problemAdmin(admin.ModelAdmin):
	list_display = ('exam_id', 'problem_id')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
	list_display = ('title',)
