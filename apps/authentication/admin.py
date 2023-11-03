from django.contrib import admin

from .models import (
    User,
    Student,
    Teacher,
    Parent,
    Group,
    Lesson,
    StudentProfile,
    TeacherProfile,
    Attendance,
    Mark
)

# inline uchun ko'dlar

# class MembershipInline(admin.TabularInline):
#     model = Membership
#     read_only_fields = ['student', 'group', 'user']
#     extra = 1

# class GroupInline(admin.TabularInline):
#     model = Group
#     extra = 1

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     inlines = [MembershipInline]

# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     inlines = [MembershipInline]

models = [User, Student, Teacher, Parent, Group, StudentProfile, TeacherProfile, Lesson, Attendance, Mark]

for model in models:
    admin.site.register(model)
