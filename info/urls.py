from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('student/<slug:id>/attendance/', views.attendance, name='attendance'),
    # path('student/<slug:stud_id>/<slug:course_id>/attendance/', views.attendance_detail, name='attendance_detail'),
    path('teacher/<slug:teacher_id>/<int:id>/all/', views.all_student_attendance, name='all_std_attendance'),
    # path('teacher/<int:assign_id>/ClassDates/', views.t_class_date, name='t_class_date'),
    # path('teacher/<slug:stud_id>/<slug:course_id>/attendance/', views.t_attendance_detail, name='t_attendance_detail'),
    # path('teacher/<int:att_id>/change_attendance/', views.change_att, name='change_att'),


    path('student/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    path('student/', views.StudentList.as_view(), name='student-list'),
    path('teacher/<int:pk>/', views.TeacherDetail.as_view(), name='teacher-detail'),
    path('teacher/', views.TeacherList.as_view(), name='teacher-list'),
    path('attendance/<int:pk>/', views.AttendanceDetail.as_view(), name='attendance-detail'),
    path('attendance/', views.AttendanceList.as_view(), name='attendance-list'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('user/', views.UserList.as_view(), name='user-list'),

]
