from django.core.management.base import BaseCommand
from django.utils import timezone

from assessments.models import TestResult


class Command(BaseCommand):
    help = "Remove expired anonymous test results."

    def handle(self, *args, **options):
        deleted_count, _ = TestResult.objects.filter(
            user__isnull=True,
            is_guest=True,
            expires_at__lt=timezone.now(),
        ).delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} expired guest test result(s)."))
