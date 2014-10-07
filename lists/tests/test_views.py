from django.test import TestCase
from django.utils.html import escape
from lists.models import Item, List
from lists.forms import ItemForm,  EXPECTED_ERROR_


class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        other_list_ = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list_)
        Item.objects.create(text='other list item 2', list=other_list_)

        response = self.client.get('/lists/%d/' % (list_.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()

        self.client.post('/lists/%d/' % (correct_list.id,),
                         data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        correct_list = List.objects.create()
        response = self.client.post('/lists/%d/' % correct_list.id,
                                    data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_validation_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % list_.id,
            data={'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape(EXPECTED_ERROR_)
        self.assertContains(response, expected_error)


class NewListTest(TestCase):

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape(EXPECTED_ERROR_)
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={"item_text": ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)