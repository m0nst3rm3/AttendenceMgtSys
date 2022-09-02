from datetime import timedelta
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Class, Student, Teacher
from .models import User

# Register your models here.

days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'semester')
    search_fields = ('id', 'semester')
    ordering = ['semester']
    inlines = [StudentInline]


class StudentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name')
    search_fields = ('serial_number', 'name')
    ordering = ['serial_number']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']


admin.site.register(User, UserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
