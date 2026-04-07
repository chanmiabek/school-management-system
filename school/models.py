from django.db import models
from django.conf import settings
import uuid


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Subject(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey('student.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    credit_hours = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.code})"


class FeeCollection(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ("Cash", "Cash"),
        ("Bank", "Bank"),
        ("Mobile Money", "Mobile Money"),
    )

    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    reference = models.CharField(max_length=40, unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.first_name if self.student else 'Unknown'} - {self.amount}"


class Expense(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"


class Salary(models.Model):
    teacher = models.ForeignKey('student.Teacher', on_delete=models.CASCADE, null=True)
    month = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.teacher.first_name if self.teacher else 'Unknown'} - {self.month}/{self.year}"


class Holiday(models.Model):
    title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class FeeStructure(models.Model):
    class_name = models.CharField(max_length=80)
    term = models.CharField(max_length=40)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.class_name} - {self.term}"


class Exam(models.Model):
    name = models.CharField(max_length=120)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    exam_date = models.DateField()
    total_marks = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=150)
    event_date = models.DateField()
    location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class TimeTableEntry(models.Model):
    DAY_CHOICES = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    )

    class_name = models.CharField(max_length=80)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey('student.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_name} {self.day}"


class LibraryBook(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=120)
    isbn = models.CharField(max_length=30, unique=True)
    copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class SportsActivity(models.Model):
    activity_name = models.CharField(max_length=120)
    coach_name = models.CharField(max_length=120, blank=True)
    activity_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.activity_name


class HostelRecord(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, null=True)
    room_number = models.CharField(max_length=20)
    check_in_date = models.DateField()
    guardian_contact = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.student.first_name if self.student else 'Unknown'} - {self.room_number}"


class TransportRoute(models.Model):
    route_name = models.CharField(max_length=120)
    driver_name = models.CharField(max_length=120)
    vehicle_number = models.CharField(max_length=30)
    pickup_time = models.TimeField()

    def __str__(self):
        return self.route_name
