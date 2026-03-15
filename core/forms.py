from django import forms
from .models import Student, Teacher, Subject, SchoolClass, Attendance, Exam

# -------------------------
# STUDENT FORM
# -------------------------
class StudentForm(forms.ModelForm):

    parent_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class':'border rounded px-2 py-1 w-full'})
    )

    parent_phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class':'border rounded px-2 py-1 w-full'})
    )

    class Meta:
        model = Student
        fields = ['student_id', 'name', 'grade', 'section', 'parent_name', 'monthly_fee']

        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'name': forms.TextInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),

            'grade': forms.Select(
                attrs={'class': 'border rounded px-2 py-1 w-full'},
                choices=[
                    ('Grade 1','Grade 1'),
                    ('Grade 2','Grade 2'),
                    ('Grade 3','Grade 3')
                ]
            ),

            'section': forms.Select(
                attrs={'class': 'border rounded px-2 py-1 w-full'},
                choices=[('A','A'),('B','B')]
            ),

            'parent_name': forms.TextInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'monthly_fee': forms.NumberInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),
        }

# -------------------------
# TEACHER FORM
# -------------------------from django import forms
from .models import Teacher, SchoolClass, Subject

class TeacherForm(forms.ModelForm):
    username = forms.CharField(required=True, help_text="Teacher login username")
    password = forms.CharField(required=True, widget=forms.PasswordInput, help_text="Teacher login password")

    # Dynamic fields
    classes = forms.ModelMultipleChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.SelectMultiple(attrs={'class':'border rounded px-2 py-1 w-full'}),
        required=True
    )

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'class':'border rounded px-2 py-1 w-full'}),
        required=True
    )

    class Meta:
        model = Teacher
        fields = ['name', 'phone', 'level', 'salary', 'classes', 'subjects', 'cv']
        widgets = {
            'name': forms.TextInput(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'phone': forms.TextInput(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'level': forms.Select(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'salary': forms.NumberInput(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'cv': forms.FileInput(attrs={'class':'w-full'}),
        }

# -------------------------
# SUBJECT FORM
# -------------------------
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name','level']
        widgets = {
            'name': forms.TextInput(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'level': forms.Select(attrs={'class':'border rounded px-2 py-1 w-full'}),
        }


# -------------------------
# SCHOOL CLASS FORM
# -------------------------
class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ['name', 'section', 'level']
        widgets = {
            'name': forms.TextInput(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'section': forms.TextInput(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'level': forms.Select(attrs={'class':'border rounded px-2 py-1 w-full'}),
        }

# -------------------------
# ATTENDANCE FORM
# -------------------------
from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']  # note ka saar
        widgets = {
            'student': forms.Select(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'date': forms.DateInput(attrs={'type':'date','class':'border rounded px-2 py-1 w-full'}),
            'status': forms.CheckboxInput(attrs={'class':'toggle-checkbox peer sr-only'}),
        }        

# -------------------------
# EXAM FORM
# -------------------------from .models import Exam, SchoolClass, Subject

class ExamForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class':'border rounded px-2 py-1 w-full'}),
        required=True
    )

    school_class = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={'class':'border rounded px-2 py-1 w-full'}),
        required=True
    )

    class Meta:
        model = Exam
        fields = ['title','subject','school_class','date','total_marks','notes']
        widgets = {
            'title': forms.TextInput(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'date': forms.DateInput(attrs={'type':'date','class':'border rounded px-2 py-1 w-full'}),
            'total_marks': forms.NumberInput(attrs={'class':'border rounded px-2 py-1 w-full'}),
            'notes': forms.Textarea(attrs={'class':'border rounded px-2 py-1 w-full', 'rows':2}),
        }