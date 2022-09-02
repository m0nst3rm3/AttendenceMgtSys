from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Student, Attendance, Course, Teacher, Assign, AttendanceTotal
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.


@login_required
def index(request):
    if request.user.is_teacher:
        return render(request, 'info/t_homepage.html')
    if request.user.is_student:
        return render(request, 'info/homepage.html')
    return render(request, 'info/logout.html')


@login_required()
def attendance(request, stud_id):
    student = Student.objects.get(serial_number=stud_id)
    ass_list = Assign.objects.filter(class_id_id=student.class_id)
    att_list = []
    for ass in ass_list:
        try:
            a = AttendanceTotal.objects.get(student=student, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=student, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'info/attendance.html', {'att_list': att_list})


@login_required()
def attendance_detail(request, stud_id, course_id):
    stud = get_object_or_404(Student, serial_number=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    return render(request, 'info/att_detail.html', {'att_list': att_list, 'cr': cr})


# Teacher Views

@login_required
def t_clas(request, teacher_id, choice):
    teacher1 = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'info/t_clas.html', {'teacher1': teacher1, 'choice': choice})


@login_required()
def t_class_date(request, assign_id):
    now = timezone.now()
    ass = get_object_or_404(Assign, id=assign_id)
    att_list = ass.attendanceclass_set.filter(date__lte=now).order_by('-date')
    return render(request, 'info/t_class_date.html', {'att_list': att_list})

@login_required()
def t_attendance_detail(request, stud_id, course_id):
    stud = get_object_or_404(Student, serial_number=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    return render(request, 'info/t_att_detail.html', {'att_list': att_list, 'cr': cr})


@login_required()
def change_att(request, att_id):
    a = get_object_or_404(Attendance, id=att_id)
    a.status = not a.status
    a.save()
    return HttpResponseRedirect(reverse('t_attendance_detail', args=(a.student.serial_number, a.course_id)))


@login_required()
def t_extra_class(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
    }
    return render(request, 'info/t_extra_class.html', context)


@login_required()
def e_confirm(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    cr = ass.course
    cl = ass.class_id
    assc = ass.attendanceclass_set.create(status=1, date=request.POST['date'])
    assc.save()

    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.serial_number]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        date = request.POST['date']
        a = Attendance(course=cr, student=s, status=status, date=date, attendanceclass=assc)
        a.save()

    return HttpResponseRedirect(reverse('t_clas', args=(ass.teacher_id, 1)))
