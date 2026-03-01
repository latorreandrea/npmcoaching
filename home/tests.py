from django.test import TestCase
from django.urls import reverse


class HomePublicPagesTests(TestCase):
	def test_home_page_renders(self):
		response = self.client.get(reverse('home-index'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/index.html')
		self.assertContains(response, 'id="cookie-consent"', html=False)
		self.assertContains(response, 'role="dialog"', html=False)
		self.assertContains(response, 'data-cookie-action="accept"', html=False)
		self.assertContains(response, 'data-cookie-action="reject"', html=False)
		self.assertContains(response, 'data-cookie-action="save"', html=False)
		self.assertContains(response, 'id="open-cookie-preferences"', html=False)

	def test_privacy_page_renders(self):
		response = self.client.get(reverse('privacy-policy'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/privacy.html')
		self.assertContains(response, 'Diritti dell’utente')
		self.assertContains(response, 'accesso, rettifica, cancellazione, limitazione del trattamento e portabilità')
		self.assertContains(response, 'non viene salvato nello storico permanente')
		self.assertContains(response, 'sessione tecnica attiva')

	def test_cookie_page_renders(self):
		response = self.client.get(reverse('cookie-policy'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/cookie.html')
		self.assertContains(response, 'Cookie tecnici per test ospite')
		self.assertContains(response, 'rimane disponibile solo nella sessione tecnica corrente')
		self.assertContains(response, 'solo dopo accesso o registrazione volontaria')

	def test_terms_page_renders(self):
		response = self.client.get(reverse('terms-conditions'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/terms.html')
		self.assertContains(response, 'Dati e riservatezza')
		self.assertContains(response, 'non vengono salvati nello storico permanente')
