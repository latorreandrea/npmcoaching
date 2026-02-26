from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

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
