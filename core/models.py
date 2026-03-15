from django.db import models
from django.contrib.auth.models import User

# -------------------------
# STUDENT
# -------------------------
class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    parent_name = models.CharField(max_length=100)
    monthly_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.student_id} - {self.name}"


# -------------------------
# TEACHER
# -------------------------
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    level = models.CharField(max_length=50, choices=[('Primary','Primary'),('Secondary','Secondary')],blank=True,null=True)
    salary = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    classes = models.ManyToManyField('SchoolClass', blank=True)
    subjects = models.ManyToManyField('Subject', blank=True)
    cv = models.FileField(upload_to='teacher_cvs/', blank=True, null=True)

    def __str__(self):
        return self.name


# -------------------------
# PARENT
# -------------------------
class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.student.name})"


# -------------------------
# SUBJECT
# -------------------------
class Subject(models.Model):
    LEVEL_CHOICES = [
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
    ]

    name = models.CharField(max_length=100, unique=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='Primary')

    def __str__(self):
        return f"{self.name} ({self.level})"
    

# -------------------------
# SCHOOL CLASS
# -------------------------
class SchoolClass(models.Model):
    LEVEL_CHOICES = [
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
    ]

    name = models.CharField(max_length=50, unique=True)
    section = models.CharField(max_length=10, blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='Primary')

    def __str__(self):
        if self.section:
            return f"{self.name} - {self.section} ({self.level})"
        return f"{self.name} ({self.level})"
    

# -------------------------
# ATTENDANCE
# -------------------------
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'date', 'teacher')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.get_status_display()} ({self.teacher.name})"


# -------------------------
# EXAMS
# -------------------------
class Exam(models.Model):
    title = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    date = models.DateField()
    total_marks = models.IntegerField(default=100)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.school_class} - {self.subject}"