from datetime import date

from django.shortcuts import render, get_object_or_404
from .models import Assign, AttendanceTotal
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    attendance_check = date.today()
    if request.user.is_teacher:
        return render(request, 'info/t_homepage.html', {'user': request.user})
    if request.user.is_student:
        std = Student.objects.filter(user=request.user.id)
        if not Attendance.objects.filter(student=std[0], daily_login=attendance_check).exists():
            Attendance.objects.create(student=std[0], daily_login=attendance_check)
        return render(request, 'info/homepage.html', {'user': request.user})
    return render(request, 'info/logout.html')


@login_required()
def attendance(request, id):
    data = {}

    attendance1 = Attendance.objects.filter(daily_login=date.today()).first()
    data[attendance1] = attendance1.daily_login if "Present" else "Absent"
    return render(request, 'info/attendance.html', context={"data": data})


@login_required()
def attendance_detail(request, id):
    stud = get_object_or_404(Student, serial_number=id)
    att_list = Attendance.objects.filter(student=stud).order_by('date')
    return render(request, 'info/att_detail.html', {'att_list': att_list})


# Teacher Views

@login_required
def all_student_attendance(request, *args, **kwargs):
    data = []
    for student in Student.objects.all():
        student_info = {"name": student.full_name}
        att = student.attendances.filter(daily_login=date.today()).first()
        status = "Present" if att else "Absent"
        student_info["status"] = status
        student_info["total_attendance"] = student.attendances.count()
        data.append(student_info)
    return render(request, 'info/all_student_attendance.html', context={"data": data})


from info.models import User, Teacher, Student, Class, Attendance
from info.serializers import UserSerializer, ClassSerializer, StudentSerializer, TeacherSerializer, AttendanceSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class UserList(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StudentList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'info/all_student_attendance.html'

    def get(self, request):
        queryset = Student.objects.all()
        # import ipdb; ipdb.set_trace()
        return Response({'student': queryset})


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class ClassList(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class AttendanceList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


