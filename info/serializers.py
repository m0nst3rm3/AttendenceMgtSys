# from rest_framework import serializers
# from .models import Deptpar, Class, Course, Student, Teacher, Attendance, AttendanceClass, Assign,  StudentCourse, sex_choice
#
#
# class StudentSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     USN = serializers.CharField(max_length=100)
#     name = serializers.CharField(required=True, max_length=200)
#     sex = serializers.CharField(max_length=sex_choice, default='Male')
#     DOB = serializers.DateField(default='1998-01-01')
#
#     def create(self, validated_data):
#         return Student.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.USN = validated_data.get('USN', instance.USN)
#         instance.name = validated_data.get('name', instance.name)
#         instance.sex = validated_data.get('sex', instance.sex)
#         instance.DOB = validated_data.get('DOB', instance.DOB)
#
#
