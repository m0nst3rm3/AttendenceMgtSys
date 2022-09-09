from rest_framework import serializers
from .models import Class, Student, Teacher, Attendance, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # student = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all())
    # teacher = serializers.PrimaryKeyRelatedField(many=True, queryset=Teacher.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'student', 'teacher']


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ['semester']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    # student = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Attendance
        # fields = ['daily_login']
        fields = "__all__"
