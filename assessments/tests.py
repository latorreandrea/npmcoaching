from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Answer, GuestConsentLog, PersonalityProfile, Question, Test, TestResult


class AssessmentsGuestAndUserFlowTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username="utente_assessment",
            email="utente_assessment@example.com",
            password="PasswordSicura123!",
        )
        self.other_user = self.user_model.objects.create_user(
            username="altro_utente",
            email="altro_utente@example.com",
            password="PasswordSicura123!",
        )

        self.test_obj = Test.objects.create(
            title="Test Comunicazione",
            description="Descrizione test",
            is_active=True,
        )
        self.question = Question.objects.create(test=self.test_obj, text="Domanda 1", order=1)
        self.answer_low = Answer.objects.create(question=self.question, text="Risposta A", points=2, order=1)
        self.answer_high = Answer.objects.create(question=self.question, text="Risposta B", points=8, order=2)
        self.personality = PersonalityProfile.objects.create(
            test=self.test_obj,
            name="Profilo Bilanciato",
            description="Descrizione profilo",
            min_score=0,
            max_score=10,
        )

    def _post_test(self, client, answer, guest_consent=True):
        client.get(reverse("assessments:take-test", args=[self.test_obj.id]))
        payload = {f"question_{self.question.id}": str(answer.id)}
        if guest_consent:
            payload["guest_consent"] = "on"
        return client.post(
            reverse("assessments:take-test", args=[self.test_obj.id]),
            data=payload,
        )

    def test_guest_can_view_test_list(self):
        response = self.client.get(reverse("assessments:tests-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assessments/tests_list.html")

    def test_guest_can_take_test_and_view_own_result(self):
        response = self._post_test(self.client, self.answer_high)
        self.assertEqual(response.status_code, 302)

        result = TestResult.objects.latest("id")
        self.assertTrue(result.is_guest)
        self.assertIsNone(result.user)
        self.assertTrue(result.session_key)

        result_page = self.client.get(reverse("assessments:test-result", args=[result.id]))
        self.assertEqual(result_page.status_code, 200)
        self.assertContains(result_page, "Risultato temporaneo in modalità ospite")
        self.assertEqual(GuestConsentLog.objects.filter(test=self.test_obj).count(), 1)

    def test_guest_submit_requires_explicit_consent(self):
        response = self._post_test(self.client, self.answer_high, guest_consent=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "devi accettare Privacy e Cookie Policy")
        self.assertEqual(TestResult.objects.count(), 0)
        self.assertEqual(GuestConsentLog.objects.count(), 0)

    def test_guest_cannot_view_result_from_other_session(self):
        self._post_test(self.client, self.answer_high)
        result = TestResult.objects.latest("id")

        second_client = self.client_class()
        response = second_client.get(reverse("assessments:test-result", args=[result.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("assessments:tests-list"))

    def test_authenticated_user_result_is_private(self):
        self.client.login(username="utente_assessment", password="PasswordSicura123!")
        self._post_test(self.client, self.answer_high)
        user_result = TestResult.objects.filter(user=self.user).latest("id")

        other_client = self.client_class()
        other_client.login(username="altro_utente", password="PasswordSicura123!")
        response = other_client.get(reverse("assessments:test-result", args=[user_result.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.url)

    def test_guest_results_are_claimed_after_login_same_session(self):
        self._post_test(self.client, self.answer_low)
        guest_result = TestResult.objects.latest("id")

        self.client.login(username="utente_assessment", password="PasswordSicura123!")

        guest_result.refresh_from_db()
        self.assertEqual(guest_result.user_id, self.user.id)
        self.assertFalse(guest_result.is_guest)
        self.assertEqual(guest_result.session_key, "")
        self.assertIsNone(guest_result.expires_at)

    @override_settings(
        ASSESSMENTS_GUEST_RATE_LIMIT_COUNT=1,
        ASSESSMENTS_GUEST_RATE_LIMIT_WINDOW_SECONDS=60,
    )
    def test_guest_rate_limit_blocks_excessive_submissions(self):
        first = self._post_test(self.client, self.answer_low)
        self.assertEqual(first.status_code, 302)

        second = self._post_test(self.client, self.answer_low)
        self.assertEqual(second.status_code, 200)
        self.assertContains(second, "Hai effettuato troppi invii in poco tempo")

    def test_take_test_page_shows_guest_consent_controls_and_policy_links(self):
        response = self.client.get(reverse("assessments:take-test", args=[self.test_obj.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="guest_consent"', html=False)
        self.assertContains(response, 'id="guest_consent"', html=False)
        self.assertContains(response, 'required', html=False)
        self.assertContains(response, reverse("privacy-policy"))
        self.assertContains(response, reverse("cookie-policy"))
        self.assertContains(response, "Domanda 1 di 1")
        self.assertContains(response, "Progresso test")
        self.assertContains(response, "Completa test")
        self.assertNotContains(response, "Indietro")

    def test_submit_with_missing_answers_shows_validation_message(self):
        self.client.get(reverse("assessments:take-test", args=[self.test_obj.id]))
        response = self.client.post(
            reverse("assessments:take-test", args=[self.test_obj.id]),
            data={"guest_consent": "on"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seleziona una risposta per continuare")
        self.assertEqual(TestResult.objects.count(), 0)

    def test_test_flow_shows_one_question_at_a_time_and_only_forward(self):
        second_question = Question.objects.create(test=self.test_obj, text="Domanda 2", order=2)
        second_answer = Answer.objects.create(question=second_question, text="Risposta C", points=4, order=1)

        first_page = self.client.get(reverse("assessments:take-test", args=[self.test_obj.id]))
        self.assertEqual(first_page.status_code, 200)
        self.assertContains(first_page, "Domanda 1 di 2")
        self.assertContains(first_page, "Domanda 1")
        self.assertNotContains(first_page, "Domanda 2")
        self.assertContains(first_page, "Avanti")
        self.assertNotContains(first_page, "Indietro")

        next_step = self.client.post(
            reverse("assessments:take-test", args=[self.test_obj.id]),
            data={f"question_{self.question.id}": str(self.answer_low.id)},
        )
        self.assertEqual(next_step.status_code, 302)

        second_page = self.client.get(reverse("assessments:take-test", args=[self.test_obj.id]))
        self.assertEqual(second_page.status_code, 200)
        self.assertContains(second_page, "Domanda 2 di 2")
        self.assertContains(second_page, "Domanda 2")
        self.assertNotContains(second_page, "Domanda 1")
        self.assertContains(second_page, "Completa test")
        self.assertNotContains(second_page, "Indietro")

        final_submit = self.client.post(
            reverse("assessments:take-test", args=[self.test_obj.id]),
            data={
                f"question_{second_question.id}": str(second_answer.id),
                "guest_consent": "on",
            },
        )
        self.assertEqual(final_submit.status_code, 302)
        self.assertEqual(TestResult.objects.count(), 1)

    @override_settings(ASSESSMENTS_GUEST_CONSENT_POLICY_VERSION="2026-03")
    def test_guest_consent_log_saves_configured_policy_version(self):
        response = self._post_test(self.client, self.answer_high)
        self.assertEqual(response.status_code, 302)

        consent = GuestConsentLog.objects.latest("id")
        self.assertEqual(consent.policy_version, "2026-03")

    @override_settings(ASSESSMENTS_GUEST_RESULT_RETENTION_DAYS=30)
    def test_guest_result_expiration_respects_retention_setting(self):
        response = self._post_test(self.client, self.answer_high)
        self.assertEqual(response.status_code, 302)

        result = TestResult.objects.latest("id")
        self.assertIsNotNone(result.expires_at)
        expected_min = timezone.now() + timedelta(days=30) - timedelta(seconds=5)
        expected_max = timezone.now() + timedelta(days=30) + timedelta(seconds=5)
        self.assertGreaterEqual(result.expires_at, expected_min)
        self.assertLessEqual(result.expires_at, expected_max)

    def test_expired_guest_result_is_not_accessible_even_same_session(self):
        self._post_test(self.client, self.answer_high)
        result = TestResult.objects.latest("id")
        result.expires_at = timezone.now() - timedelta(seconds=1)
        result.save(update_fields=["expires_at"])

        response = self.client.get(reverse("assessments:test-result", args=[result.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("assessments:tests-list"))

    def test_cleanup_command_deletes_only_expired_guest_results(self):
        expired_guest = TestResult.objects.create(
            user=None,
            test=self.test_obj,
            score=1,
            personality=self.personality,
            session_key="a" * 64,
            is_guest=True,
            expires_at=timezone.now() - timedelta(days=1),
        )
        active_guest = TestResult.objects.create(
            user=None,
            test=self.test_obj,
            score=2,
            personality=self.personality,
            session_key="b" * 64,
            is_guest=True,
            expires_at=timezone.now() + timedelta(days=1),
        )
        user_result = TestResult.objects.create(
            user=self.user,
            test=self.test_obj,
            score=3,
            personality=self.personality,
            is_guest=False,
            expires_at=timezone.now() - timedelta(days=1),
        )

        output = StringIO()
        call_command("cleanup_guest_test_results", stdout=output)

        self.assertFalse(TestResult.objects.filter(id=expired_guest.id).exists())
        self.assertTrue(TestResult.objects.filter(id=active_guest.id).exists())
        self.assertTrue(TestResult.objects.filter(id=user_result.id).exists())
        self.assertIn("Deleted 1 expired guest test result(s).", output.getvalue())
