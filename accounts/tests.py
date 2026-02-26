from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountUserFlowTests(TestCase):
	def setUp(self):
		self.user_model = get_user_model()
		self.user = self.user_model.objects.create_user(
			username='utente',
			email='utente@example.com',
			password='PasswordSicura123!'
		)
		self.admin = self.user_model.objects.create_superuser(
			username='admin',
			email='admin@example.com',
			password='PasswordSicura123!'
		)

	def test_profile_requires_authentication(self):
		response = self.client.get(reverse('accounts:profile'))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('account_login'), response.url)

	def test_profile_page_is_available_for_authenticated_user(self):
		self.client.login(username='utente', password='PasswordSicura123!')
		response = self.client.get(reverse('accounts:profile'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/profile.html')

	def test_admin_dashboard_requires_superuser(self):
		self.client.login(username='utente', password='PasswordSicura123!')
		response = self.client.get(reverse('accounts:admin-dashboard'))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('account_login'), response.url)

	def test_admin_dashboard_is_available_for_superuser(self):
		self.client.login(username='admin', password='PasswordSicura123!')
		response = self.client.get(reverse('accounts:admin-dashboard'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/admin_dashboard.html')

	def test_login_page_renders(self):
		response = self.client.get(reverse('account_login'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'account/login.html')

	def test_signup_page_renders(self):
		response = self.client.get(reverse('account_signup'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'account/signup.html')
