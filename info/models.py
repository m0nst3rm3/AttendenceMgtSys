from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import datetime

# Create your models here.
sex_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

time_slots = (
    ('7:30 - 8:30', '7:30 - 8:30'),
    ('8:30 - 9:30', '8:30 - 9:30'),
    ('9:30 - 10:30', '9:30 - 10:30'),
    ('11:00 - 11:50', '11:00 - 11:50'),
    ('11:50 - 12:40', '11:50 - 12:40'),
    ('12:40 - 1:30', '12:40 - 1:30'),
    ('2:30 - 3:30', '2:30 - 3:30'),
    ('3:30 - 4:30', '3:30 - 4:30'),
    ('4:30 - 5:30', '4:30 - 5:30'),
)

DAYS_OF_WEEK = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
)

test_name = (
    ('Internal test 1', 'Internal test 1'),
    ('Internal test 2', 'Internal test 2'),
    ('Internal test 3', 'Internal test 3'),
    ('Event 1', 'Event 1'),
    ('Event 2', 'Event 2'),
    ('Semester End Exam', 'Semester End Exam'),
)


class User(AbstractUser):
    @property
    def is_student(self):
        if hasattr(self, 'student'):
            return True
        return False

    @property
    def is_teacher(self):
        if hasattr(self, 'teacher'):
            return True
        return False


class Course(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Class(models.Model):
    semester = models.IntegerField()

    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        return '%d' % (self.semester)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, default=1)
    serial_number = models.CharField(primary_key='True', max_length=100)
    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=6, choices=sex_choice, default='Male')
    DOB = models.DateField(default='1998-01-01')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=6, choices=sex_choice, default='Male')
    DOB = models.DateField(default='1980-01-01')

    def __str__(self):
        return self.name


class Assign(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('course', 'class_id', 'teacher'),)

    def __str__(self):
        return '%s : %s : %s' % (self.teacher.name, self.course.shortname, self.class_id)


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    daily_login = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return '%s : %s' % (self.student.name, self.course.shortname)


class AttendanceTotal(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'course'),)

    @property
    def total_class(self):
        student = Student.objects.get(name=self.student)
        course = Course.objects.get(name=self.course)
        total_class = Attendance.objects.filter(course=course, student=student).count()
        return total_class

    @property
    def attendance(self):
        student = Student.objects.get(name=self.student)
        course = Course.objects.get(name=self.course)
        total_class = Attendance.objects.filter(course=course, student=student).count()
        att_class = Attendance.objects.filter(course=course, student=student, status='True').count()
        if total_class == 0:
            attendance = 0
        else:
            attendance = round(att_class / total_class * 100, 2)
        return attendance
