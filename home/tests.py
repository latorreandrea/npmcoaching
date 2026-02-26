from django.test import TestCase
from django.urls import reverse


class HomePublicPagesTests(TestCase):
	def test_home_page_renders(self):
		response = self.client.get(reverse('home-index'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/index.html')

	def test_privacy_page_renders(self):
		response = self.client.get(reverse('privacy-policy'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/privacy.html')

	def test_cookie_page_renders(self):
		response = self.client.get(reverse('cookie-policy'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/cookie.html')

	def test_terms_page_renders(self):
		response = self.client.get(reverse('terms-conditions'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/terms.html')
