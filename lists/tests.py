from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item, List
from lists.views import home_page #1


class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/') #2
		self.assertEqual(found.func, home_page) #3

	def test_home_page_return_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/'%(list_.id,))
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self):
		list_ = List.objects.create()
		Item.objects.create(text='itemey 1', list = list_)
		Item.objects.create(text='itemey 2', list = list_)

		other_list_ = List.objects.create()
		Item.objects.create(text='other list item 1', list = other_list_)
		Item.objects.create(text='other list item 2', list = other_list_)
		
		response = self.client.get('/lists/%d/'%(list_.id,))

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/'%(correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)


class ListAndItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):

		first_item_text = 'The first (ever) list item'
		second_item_text = 'The second item'

		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = first_item_text
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = second_item_text
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]

		self.assertEqual(first_saved_item.text, first_item_text)
		self.assertEqual(first_saved_item.list , list_)
		self.assertEqual(second_saved_item.text, second_item_text)
		self.assertEqual(second_saved_item.list, list_)

class NewListTest(TestCase):

	def test_home_page_can_save_a_POST_request(self):
		
		self.client.post('/lists/new', data={'item_text':'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_home_page_redirects_after_POST(self):

		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		new_list = List.objects.first()
		self.assertRedirects(response,'/lists/%d/'%(new_list.id,))

class NewItemTest(TestCase):
	"""docstring for NewItemTest"""
	def test_can_save_a_POST_request_to_an_existing_list(self):
		correct_list = List.objects.create()
		other_list = List.objects.create()

		self.client.post('/lists/%d/add_item'%(correct_list.id,), 
			data={'item_text':'A new item for an existing list'})
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)
		

	def test_redirects_to_list_view(self):
		correct_list = List.objects.create()
		other_list = List.objects.create()
		response = self.client.post('/lists/%d/add_item'%(correct_list.id), 
			data={'item_text':'A new item for an existing list'})
		self.assertRedirects(response, '/lists/%d/'%(correct_list.id,))