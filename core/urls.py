from django.urls import path
from .views import (
    base, sidebar, dashboard, navbar,
    student_dashboard, teachers_dashboard,
    add_teacher, edit_teacher, delete_teacher,
    student_add, student_edit, student_delete,
    subject_add, subject_delete, subject_edit, subject_list,
    class_add, class_edit, class_delete, class_list,
    teacher_attendance, exam_list, exam_edit, exam_add, exam_delete,
    parent_list, attendance_list
)

urlpatterns = [
    # Base / common pages
    path('base/', base, name='base'),
    path('sidebar/', sidebar, name='sidebar'),
    path('', dashboard, name='dashboard'),
    path('navbar/', navbar, name='navbar'),

    # Student pages
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('student_add/', student_add, name='student_add'),
    path('student_edit/<int:pk>/', student_edit, name='student_edit'),
    path('student_delete/<int:pk>/', student_delete, name='student_delete'),

    # Teacher pages
    path('teachers/dashboard/', teachers_dashboard, name='teachers_dashboard'),
    path('teachers/add/', add_teacher, name='add_teacher'),
    path('teachers/edit/<int:pk>/', edit_teacher, name='edit_teacher'),
    path('teachers/delete/<int:pk>/', delete_teacher, name='delete_teacher'),

    # Subjects
    path('subjects/', subject_list, name='subject_list'),
    path('subjects/add/', subject_add, name='subject_add'),
    path('subjects/edit/<int:pk>/', subject_edit, name='subject_edit'),
    path('subjects/delete/<int:pk>/', subject_delete, name='subject_delete'),

    # Classes
    path('classes/', class_list, name='class_list'),
    path('classes/add/', class_add, name='class_add'),
    path('classes/edit/<int:pk>/', class_edit, name='class_edit'),
    path('classes/delete/<int:pk>/', class_delete, name='class_delete'),

    # Attendance
    path('attendance/', attendance_list, name='attendance_list'),
    path('attendance/teacher/', teacher_attendance, name='teacher_attendance'),

    # Exams
    path('exams/', exam_list, name='exam_list'),
    path('exams/add/', exam_add, name='exam_add'),
    path('exams/edit/<int:pk>/', exam_edit, name='exam_edit'),
    path('exams/delete/<int:pk>/', exam_delete, name='exam_delete'),

    # Parents
    path('parents/', parent_list, name='parent_list'),
]