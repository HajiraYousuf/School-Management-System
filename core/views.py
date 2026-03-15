from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import date

from .models import Student, Teacher, Subject, SchoolClass, Attendance, Exam, Parent
from .forms import StudentForm, SubjectForm, SchoolClassForm, AttendanceForm, ExamForm

def base(request):
    return render(request, 'base.html')

def sidebar(request):
    return render(request,'sidebar.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def navbar(request):
    return render(request,'navbar.html')


# --- STUDENT ---
def student_dashboard(request):
    students = Student.objects.all()
    return render(request,'student_dashboard.html', {'students': students})
def student_add(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():

            student = form.save()

            Parent.objects.create(
                name=form.cleaned_data['parent_name'],
                email=form.cleaned_data['parent_email'],
                phone=form.cleaned_data['parent_phone'],
                student=student
            )

            return redirect('student_dashboard')

    else:
        form = StudentForm()

    return render(request,'student_form.html',{'form':form})
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form, 'title': 'Edit Student'})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_dashboard')
    return render(request, 'delete_confirm.html', {'item': student, 'type': 'Student'})


# --- TEACHER CRUD (modal on dashboard) ---
def teachers_dashboard(request):
    teachers = Teacher.objects.all()
    classes = SchoolClass.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'teachers_dashboard.html', {
        'teachers': teachers,
        'classes': classes,
        'subjects': subjects
    })
from .models import SchoolClass, Subject, Teacher
def add_teacher(request):
    classes = SchoolClass.objects.all()      # qaado dhammaan classes
    subjects = Subject.objects.all()   # qaado dhammaan subjects

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        level = request.POST.get('level')
        salary = request.POST.get('salary')
        cv = request.FILES.get('cv')
        selected_classes = request.POST.getlist('classes')
        selected_subjects = request.POST.getlist('subjects')

        teacher = Teacher.objects.create(
            name=name,
            phone=phone,
            level=level,
            salary=salary,
            cv=cv
        )

        # ManyToMany fields
        teacher.classes.set(selected_classes)   # assuming 'classes' is a ManyToManyField
        teacher.subjects.set(selected_subjects)

        return redirect('teachers_dashboard')

    return render(request, 'teteachers_dashboard.html', {'classes': classes, 'subjects': subjects})


from django.shortcuts import get_object_or_404, redirect, render
from .models import Teacher, SchoolClass, Subject
from .forms import TeacherForm

def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    classes = SchoolClass.objects.all()
    subjects = Subject.objects.all()

    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            teacher = form.save()
            # Update many-to-many fields
            teacher.classes.set(request.POST.getlist('classes[]'))
            teacher.subjects.set(request.POST.getlist('subjects[]'))
            return redirect('teachers_dashboard')
    else:
        form = TeacherForm(instance=teacher)

    return render(request, "edit_teacher_modal.html", {
        'form': form,
        'teacher': teacher,
        'classes': classes,
        'subjects': subjects
    })


def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        if teacher.user:
            teacher.user.delete()
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('teachers_dashboard')
    return render(request, 'teachers_dashboard.html', {'teacher': teacher})


# --- SUBJECT ---
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'form.html', {'form': form, 'title': 'Add Subject'})

def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'form.html', {'form': form, 'title': 'Edit Subject'})

def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')
    return render(request, 'delete_confirm.html', {'item': subject, 'type': 'Subject'})


# --- CLASS ---
def class_list(request):
    classes = SchoolClass.objects.all()
    return render(request, 'class_list.html', {'classes': classes})

def class_add(request):
    if request.method == 'POST':
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = SchoolClassForm()
    return render(request, 'form.html', {'form': form, 'title': 'Add Class'})

def class_edit(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    if request.method == 'POST':
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = SchoolClassForm(instance=school_class)
    return render(request, 'form.html', {'form': form, 'title': 'Edit Class'})

def class_delete(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    if request.method == 'POST':
        school_class.delete()
        return redirect('class_list')
    return render(request, 'delete_confirm.html', {'item': school_class, 'type': 'Class'})


# --- ATTENDANCE ---
def attendance_list(request):
    search_date = request.GET.get('date', date.today())
    students = Student.objects.all()
    attendance_records = Attendance.objects.filter(date=search_date)
    
    context = {
        'students': students,
        'attendance_records': attendance_records,
        'search_date': search_date,
    }
    return render(request, 'attendance_list.html', context)

def attendance_add(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'form.html', {'form': form, 'title': 'Mark Attendance'})

def attendance_edit(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=record)
    return render(request, 'form.html', {'form': form, 'title': 'Edit Attendance'})

def attendance_delete(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('attendance_list')
    return render(request, 'delete_confirm.html', {'item': record, 'type': 'Attendance'})


# --- TEACHER ATTENDANCE PAGE ---
def teacher_attendance(request):
    students = Student.objects.all()
    today = date.today()

    teacher = Teacher.objects.first()

    if request.method == "POST":
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            note = request.POST.get(f'note_{student.id}', '')

            Attendance.objects.update_or_create(
                student=student,
                teacher=teacher,
                date=today,
                defaults={'status': status, 'note': note}
            )
        return redirect('attendance_list')

    attendance_records = {a.student.id: a for a in Attendance.objects.filter(date=today, teacher=teacher)}

    context = {
        'students': students,
        'attendance_records': attendance_records,
        'today': today
    }
    return render(request, 'teacher_attendance.html', context)


# --- EXAMS ---
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exam_list.html', {'exams': exams})

def exam_add(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'form.html', {'form': form, 'title': 'Add Exam'})

def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'form.html', {'form': form, 'title': 'Edit Exam'})

def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == "POST":
        exam.delete()
        return redirect('exam_list')
    return render(request, 'delete_confirm.html', {'item': exam, 'type': 'Exam'})


# --- PARENTS ---
def parent_list(request):
    parents = Parent.objects.all()
    return render(request, 'parent_list.html', {'parents': parents})