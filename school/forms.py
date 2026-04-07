from django import forms
from .models import (
    Department,
    Exam,
    Event,
    Expense,
    FeeCollection,
    FeeStructure,
    Holiday,
    HostelRecord,
    LibraryBook,
    Salary,
    SportsActivity,
    Subject,
    TimeTableEntry,
    TransportRoute,
)
from student.models import Teacher, Student

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "code", "description"]

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            "user",
            "first_name",
            "last_name",
            "teacher_id",
            "email",
            "mobile_number",
            "gender",
            "department",
            "joining_date",
            "address",
        ]
        widgets = {"joining_date": forms.DateInput(attrs={"type": "date"})}

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "code", "department", "teacher", "credit_hours"]

class FeeCollectionForm(forms.ModelForm):
    class Meta:
        model = FeeCollection
        fields = ["student", "amount", "paid_on", "payment_method", "reference", "notes"]
        widgets = {"paid_on": forms.DateInput(attrs={"type": "date"})}

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "category", "amount", "expense_date", "notes"]
        widgets = {"expense_date": forms.DateInput(attrs={"type": "date"})}

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ["teacher", "month", "year", "amount", "paid_on", "notes"]
        widgets = {"paid_on": forms.DateInput(attrs={"type": "date"})}

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ["title", "start_date", "end_date", "description"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ["class_name", "term", "amount", "due_date"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["name", "subject", "exam_date", "total_marks"]
        widgets = {"exam_date": forms.DateInput(attrs={"type": "date"})}

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "event_date", "location", "description"]
        widgets = {"event_date": forms.DateInput(attrs={"type": "date"})}

class TimeTableEntryForm(forms.ModelForm):
    class Meta:
        model = TimeTableEntry
        fields = ["class_name", "day", "subject", "teacher", "start_time", "end_time"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

class LibraryBookForm(forms.ModelForm):
    class Meta:
        model = LibraryBook
        fields = ["title", "author", "isbn", "copies_available"]

class SportsActivityForm(forms.ModelForm):
    class Meta:
        model = SportsActivity
        fields = ["activity_name", "coach_name", "activity_date", "notes"]
        widgets = {"activity_date": forms.DateInput(attrs={"type": "date"})}

class HostelRecordForm(forms.ModelForm):
    class Meta:
        model = HostelRecord
        fields = ["student", "room_number", "check_in_date", "guardian_contact"]
        widgets = {"check_in_date": forms.DateInput(attrs={"type": "date"})}

class TransportRouteForm(forms.ModelForm):
    class Meta:
        model = TransportRoute
        fields = ["route_name", "driver_name", "vehicle_number", "pickup_time"]
        widgets = {"pickup_time": forms.TimeInput(attrs={"type": "time"})}
