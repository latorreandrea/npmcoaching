from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models import Q
from django.utils import timezone

from .models import TestResult
from .utils import session_fingerprint


def claim_guest_results_for_user(*, user, session_key):
    if not user or not session_key:
        return 0

    keys = [session_fingerprint(session_key)]

    updated = TestResult.objects.filter(
        user__isnull=True,
        is_guest=True,
        session_key__in=keys,
    ).filter(Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now()))

    count = updated.update(
        user=user,
        is_guest=False,
        session_key="",
        expires_at=None,
    )
    return count


@receiver(user_logged_in)
def claim_guest_results_on_login(sender, request, user, **kwargs):
    if not request or not request.session:
        return

    session_key = request.session.session_key
    current_fingerprint = session_fingerprint(session_key)
    preserved_fingerprint = request.session.get("assessments_guest_fingerprint", "")
    keys = [key for key in {current_fingerprint, preserved_fingerprint} if key]

    if not keys:
        return

    updated = TestResult.objects.filter(
        user__isnull=True,
        is_guest=True,
        session_key__in=keys,
    ).filter(Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now()))

    updated.update(
        user=user,
        is_guest=False,
        session_key="",
        expires_at=None,
    )
    request.session.pop("assessments_guest_fingerprint", None)
