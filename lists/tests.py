from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page #1

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/') #2
		self.assertEqual(found.func, home_page) #3

	def test_home_page_return_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>To-Do lists</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))