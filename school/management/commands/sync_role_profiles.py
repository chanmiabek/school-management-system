from django.core.management.base import BaseCommand
from django.db import transaction

from home_auth.models import CustomUser
from school.models import Teacher
from student.models import Student


class Command(BaseCommand):
    help = "Sync role flags and link Teacher/Student profiles to users."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show changes without saving.")

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        teacher_links = self._link_teachers(dry_run=dry_run)
        student_links = self._link_students(dry_run=dry_run)
        role_updates = self._sync_roles(dry_run=dry_run)

        if dry_run:
            transaction.set_rollback(True)

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Teacher links: {teacher_links}, Student links: {student_links}, Role updates: {role_updates}"
            )
        )

    def _link_teachers(self, dry_run=False):
        updates = 0
        users_by_email = {u.email.lower(): u for u in CustomUser.objects.exclude(email="")}
        for teacher in Teacher.objects.filter(user__isnull=True):
            user = users_by_email.get((teacher.email or "").lower())
            if not user:
                matches = CustomUser.objects.filter(
                    first_name__iexact=teacher.first_name,
                    last_name__iexact=teacher.last_name,
                    is_teacher=True,
                )
                if matches.count() == 1:
                    user = matches.first()
            if user and not Teacher.objects.filter(user=user).exclude(id=teacher.id).exists():
                teacher.user = user
                if not dry_run:
                    teacher.save(update_fields=["user"])
                updates += 1
        return updates

    def _link_students(self, dry_run=False):
        updates = 0
        for student in Student.objects.filter(user__isnull=True):
            matches = CustomUser.objects.filter(
                first_name__iexact=student.first_name,
                last_name__iexact=student.last_name,
                is_student=True,
            )
            if matches.count() == 1:
                user = matches.first()
                if not Student.objects.filter(user=user).exclude(id=student.id).exists():
                    student.user = user
                    if not dry_run:
                        student.save(update_fields=["user"])
                    updates += 1
        return updates

    def _sync_roles(self, dry_run=False):
        updates = 0
        teacher_user_ids = set(Teacher.objects.exclude(user__isnull=True).values_list("user_id", flat=True))
        student_user_ids = set(Student.objects.exclude(user__isnull=True).values_list("user_id", flat=True))

        for user in CustomUser.objects.all():
            new_is_admin = user.is_superuser or user.is_admin
            new_is_teacher = user.id in teacher_user_ids or user.is_teacher
            new_is_student = user.id in student_user_ids or user.is_student

            if (user.is_admin, user.is_teacher, user.is_student) != (
                new_is_admin,
                new_is_teacher,
                new_is_student,
            ):
                user.is_admin = new_is_admin
                user.is_teacher = new_is_teacher
                user.is_student = new_is_student
                if not dry_run:
                    user.save(update_fields=["is_admin", "is_teacher", "is_student"])
                updates += 1

        return updates
