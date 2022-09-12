from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
sex_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

DAYS_OF_WEEK = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
)


class AbstractUserDetail(models.Model):
    sex = models.CharField(max_length=6, choices=sex_choice, default='Male')
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser, AbstractUserDetail):
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


class Class(models.Model):
    semester = models.IntegerField()

    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        return '%d' % self.semester


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, default=1)

    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.first_name


class Assign(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('class_id', 'teacher')

    def __str__(self):
        return '%s : %s' % (self.teacher.name, self.class_id)


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    daily_login = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return '%s : %s' % (self.student.user.first_name, self.daily_login)


class AttendanceTotal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    @property
    def total_class(self):

        student = Student.objects.get(name=self.student)
        total_class = Attendance.objects.filter(student=student).count()
        return total_class

    @property
    def attendance(self):
        student = Student.objects.get(name=self.student)
        total_class = Attendance.objects.filter(student=student).count()
        att_class = Attendance.objects.filter(student=student, status='True').count()
        if total_class == 0:
            attendance = 0
        else:
            attendance = round(att_class / total_class * 100, 2)
        return attendance
