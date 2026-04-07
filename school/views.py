from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    DepartmentForm,
    EventForm,
    ExamForm,
    ExpenseForm,
    FeeCollectionForm,
    FeeStructureForm,
    HolidayForm,
    HostelRecordForm,
    LibraryBookForm,
    SalaryForm,
    SportsActivityForm,
    SubjectForm,
    TeacherForm,
    TimeTableEntryForm,
    TransportRouteForm,
)
from .models import (
    Department,
    Event,
    Exam,
    Expense,
    FeeCollection,
    FeeStructure,
    Holiday,
    HostelRecord,
    LibraryBook,
    Notification,
    Salary,
    SportsActivity,
    Subject,
    TimeTableEntry,
    TransportRoute,
)
from student.models import Teacher, Student

# Create your views here.


def _is_admin(user):
    return user.is_authenticated and (user.is_admin or user.is_superuser)


def _is_teacher(user):
    return user.is_authenticated and user.is_teacher


def _is_student(user):
    return user.is_authenticated and user.is_student


def _teacher_profile(user):
    return Teacher.objects.filter(user=user).first()


def _admin_only(request):
    if not _is_admin(request.user):
        return HttpResponseForbidden("Only admins can access this page.")
    return None

def index(request):
    return render(request, "authentication/login.html")

@login_required(login_url='login')
def dashboard(request):
    return render(request, "students/student-dashboard.html")


@login_required(login_url='login')
def mark_notification_as_read(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()

@login_required(login_url='login')
def clear_all_notification(request):
    if request.method == "POST":
        notification = Notification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()


@login_required(login_url='login')
def app_page(request, page_title, page_description):
    if _is_student(request.user):
        return HttpResponseForbidden("Students cannot access this page.")
    context = {
        "page_title": page_title,
        "page_description": page_description,
    }
    return render(request, "Home/app-page.html", context)


@login_required(login_url='login')
def profile_page(request):
    return render(request, "Home/profile.html", {"current_user": request.user})


@login_required(login_url='login')
def inbox_page(request):
    all_notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "Home/inbox.html", {"all_notifications": all_notifications})


@login_required(login_url='login')
def teacher_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    teachers = Teacher.objects.select_related("department").all().order_by("first_name", "last_name")
    return render(request, "Home/teacher-list.html", {"teachers": teachers})


@login_required(login_url='login')
def teacher_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if _is_teacher(request.user):
        current_teacher = _teacher_profile(request.user)
        if not current_teacher or current_teacher.id != teacher.id:
            return HttpResponseForbidden("Teachers can only view their own profile.")
    elif not _is_admin(request.user):
        return HttpResponseForbidden("Access denied.")
    return render(request, "Home/teacher-view.html", {"teacher": teacher})


@login_required(login_url='login')
def add_teacher(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = TeacherForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        teacher = form.save()
        messages.success(request, f"Teacher {teacher.first_name} {teacher.last_name} added successfully.")
        return redirect("teacher_list")
    return render(request, "Home/teacher-form.html", {"form": form, "page_title": "Add Teacher"})


@login_required(login_url='login')
def edit_teacher(request, teacher_id):
    denied = _admin_only(request)
    if denied:
        return denied
    teacher = get_object_or_404(Teacher, id=teacher_id)
    form = TeacherForm(request.POST or None, instance=teacher)
    if request.method == "POST" and form.is_valid():
        teacher = form.save()
        messages.success(request, f"Teacher {teacher.first_name} {teacher.last_name} updated successfully.")
        return redirect("teacher_list")
    return render(request, "Home/teacher-form.html", {"form": form, "page_title": "Edit Teacher"})


@login_required(login_url='login')
def department_list(request):
    if _is_admin(request.user):
        departments = Department.objects.all().order_by("name")
    elif _is_teacher(request.user):
        teacher = _teacher_profile(request.user)
        departments = Department.objects.filter(id=teacher.department_id) if teacher and teacher.department_id else Department.objects.none()
    else:
        return HttpResponseForbidden("Access denied.")
    return render(request, "Home/department-list.html", {"departments": departments})


@login_required(login_url='login')
def add_department(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = DepartmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        department = form.save()
        messages.success(request, f"Department {department.name} added successfully.")
        return redirect("department_list")
    return render(request, "Home/department-form.html", {"form": form, "page_title": "Add Department"})


@login_required(login_url='login')
def edit_department(request, department_id):
    denied = _admin_only(request)
    if denied:
        return denied
    department = get_object_or_404(Department, id=department_id)
    form = DepartmentForm(request.POST or None, instance=department)
    if request.method == "POST" and form.is_valid():
        department = form.save()
        messages.success(request, f"Department {department.name} updated successfully.")
        return redirect("department_list")
    return render(request, "Home/department-form.html", {"form": form, "page_title": "Edit Department"})


@login_required(login_url='login')
def subject_list(request):
    if _is_admin(request.user):
        subjects = Subject.objects.select_related("department", "teacher").all().order_by("name")
    elif _is_teacher(request.user):
        teacher = _teacher_profile(request.user)
        if teacher and teacher.department_id:
            subjects = Subject.objects.select_related("department", "teacher").filter(department_id=teacher.department_id).order_by("name")
        else:
            subjects = Subject.objects.none()
    else:
        return HttpResponseForbidden("Access denied.")
    return render(request, "Home/subject-list.html", {"subjects": subjects})


@login_required(login_url='login')
def add_subject(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = SubjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        subject = form.save()
        messages.success(request, f"Subject {subject.name} added successfully.")
        return redirect("subject_list")
    return render(request, "Home/subject-form.html", {"form": form, "page_title": "Add Subject"})


@login_required(login_url='login')
def edit_subject(request, subject_id):
    denied = _admin_only(request)
    if denied:
        return denied
    subject = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=subject)
    if request.method == "POST" and form.is_valid():
        subject = form.save()
        messages.success(request, f"Subject {subject.name} updated successfully.")
        return redirect("subject_list")
    return render(request, "Home/subject-form.html", {"form": form, "page_title": "Edit Subject"})


@login_required(login_url='login')
def fees_collection(request):
    denied = _admin_only(request)
    if denied:
        return denied
    fees = FeeCollection.objects.all().order_by("-paid_on")
    return render(request, "Home/fees-list.html", {"fees": fees})


@login_required(login_url='login')
def add_fees(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = FeeCollectionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        fee = form.save()
        messages.success(request, f"Fee for {fee.student} saved successfully.")
        return redirect("fees_collection")
    return render(request, "Home/fees-form.html", {"form": form, "page_title": "Add Fees"})


@login_required(login_url='login')
def expenses(request):
    denied = _admin_only(request)
    if denied:
        return denied
    expense_items = Expense.objects.all().order_by("-expense_date")
    return render(request, "Home/expenses-list.html", {"expense_items": expense_items})


@login_required(login_url='login')
def add_expenses(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = ExpenseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        expense = form.save()
        messages.success(request, f"Expense {expense.title} saved successfully.")
        return redirect("expenses")
    return render(request, "Home/expenses-form.html", {"form": form, "page_title": "Add Expense"})


@login_required(login_url='login')
def salary(request):
    denied = _admin_only(request)
    if denied:
        return denied
    salaries = Salary.objects.all().order_by("-paid_on")
    return render(request, "Home/salary-list.html", {"salaries": salaries})


@login_required(login_url='login')
def add_salary(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = SalaryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        salary_item = form.save()
        messages.success(request, f"Salary for {salary_item.teacher} saved successfully.")
        return redirect("salary")
    return render(request, "Home/salary-form.html", {"form": form, "page_title": "Add Salary"})


@login_required(login_url='login')
def holiday_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    holidays = Holiday.objects.all().order_by("-start_date")
    return render(request, "Home/holiday-list.html", {"holidays": holidays})


@login_required(login_url='login')
def add_holiday(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = HolidayForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Holiday added successfully.")
        return redirect("holiday")
    return render(request, "Home/holiday-form.html", {"form": form, "page_title": "Add Holiday"})


@login_required(login_url='login')
def fee_structure_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    fee_structures = FeeStructure.objects.all().order_by("class_name", "term")
    return render(request, "Home/fee-structure-list.html", {"fee_structures": fee_structures})


@login_required(login_url='login')
def add_fee_structure(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = FeeStructureForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fee structure added successfully.")
        return redirect("fees")
    return render(request, "Home/fee-structure-form.html", {"form": form, "page_title": "Add Fee Structure"})


@login_required(login_url='login')
def exam_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    exams = Exam.objects.select_related("subject").all().order_by("-exam_date")
    return render(request, "Home/exam-list.html", {"exams": exams})


@login_required(login_url='login')
def add_exam(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = ExamForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Exam added successfully.")
        return redirect("exam_list")
    return render(request, "Home/exam-form.html", {"form": form, "page_title": "Add Exam"})


@login_required(login_url='login')
def event_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    events = Event.objects.all().order_by("-event_date")
    return render(request, "Home/event-list.html", {"events": events})


@login_required(login_url='login')
def add_event(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = EventForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Event added successfully.")
        return redirect("events")
    return render(request, "Home/event-form.html", {"form": form, "page_title": "Add Event"})


@login_required(login_url='login')
def time_table_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    entries = TimeTableEntry.objects.select_related("subject", "teacher").all().order_by("day", "start_time")
    return render(request, "Home/time-table-list.html", {"entries": entries})


@login_required(login_url='login')
def add_time_table_entry(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = TimeTableEntryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Time table entry added successfully.")
        return redirect("time_table")
    return render(request, "Home/time-table-form.html", {"form": form, "page_title": "Add Time Table Entry"})


@login_required(login_url='login')
def library_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    books = LibraryBook.objects.all().order_by("title")
    return render(request, "Home/library-list.html", {"books": books})


@login_required(login_url='login')
def add_library_book(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = LibraryBookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Library book added successfully.")
        return redirect("library")
    return render(request, "Home/library-form.html", {"form": form, "page_title": "Add Book"})


@login_required(login_url='login')
def sports_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    sports = SportsActivity.objects.all().order_by("-activity_date")
    return render(request, "Home/sports-list.html", {"sports": sports})


@login_required(login_url='login')
def add_sport(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = SportsActivityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Sports activity added successfully.")
        return redirect("sports")
    return render(request, "Home/sports-form.html", {"form": form, "page_title": "Add Sports Activity"})


@login_required(login_url='login')
def hostel_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    hostels = HostelRecord.objects.all().order_by("-check_in_date")
    return render(request, "Home/hostel-list.html", {"hostels": hostels})


@login_required(login_url='login')
def add_hostel_record(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = HostelRecordForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Hostel record added successfully.")
        return redirect("hostel")
    return render(request, "Home/hostel-form.html", {"form": form, "page_title": "Add Hostel Record"})


@login_required(login_url='login')
def transport_list(request):
    denied = _admin_only(request)
    if denied:
        return denied
    routes = TransportRoute.objects.all().order_by("route_name")
    return render(request, "Home/transport-list.html", {"routes": routes})


@login_required(login_url='login')
def add_transport_route(request):
    denied = _admin_only(request)
    if denied:
        return denied
    form = TransportRouteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Transport route added successfully.")
        return redirect("transport")
    return render(request, "Home/transport-form.html", {"form": form, "page_title": "Add Transport Route"})
