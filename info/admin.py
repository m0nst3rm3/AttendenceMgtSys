from datetime import timedelta
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Class, Student, Teacher, Attendance
from .models import User

# Register your models here.


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'semester')
    search_fields = ('id', 'semester')
    ordering = ['semester']
    inlines = [StudentInline]


class StudentAdmin(admin.ModelAdmin):
    # list_display = ('name')
    search_fields = ('name', 'email')
    # ordering = ['serial_number']


class TeacherAdmin(admin.ModelAdmin):
    # list_display = ('name',)
    search_fields = ('name', 'email')
    # ordering = ['name']


admin.site.register(User, UserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Attendance)

