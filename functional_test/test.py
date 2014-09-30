from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys


class NewVisitor(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrive_it_latter(self):

#edit has hear about a cool new online to-do app. she goes
#to check out its homepage
		
		self.browser.get(self.server_url)
#she notice the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		#header_text = self.browser.find_element_by_tag_name('h1').text
		#self.assertIn('To-Do', header_text)
#she is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
				inputbox.get_attribute('placeholder'),
				'Enter a to-do item'
			)
#she types "buy peacock feathers" into a textbox(edith's hoby is tying fly-fishing lures)
		inputbox.send_keys('Buy peacock feathers')
#when hits enter, the page updates, an now the page lists
# 1: Buy a peacock feathers as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)

		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')	
		
#there is still a textbox iviting her to add another item. she
#enter "use peacock feathers to make fly"
#the page updates again, and now shos both item on her list
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		self.check_for_row_in_list_table('1: Buy peacock feathers')	
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

	
#edit wonder where the site will remember her list. then she sees that the site has generated a unique url
#for her --  the is son explanatory text to that reflect

#she visits that url - her to-do list is still there.
#satisfied , she goes back to sleep
		self.browser.quit()
		self.browser = webdriver.Firefox()

#Francis visits the home page. There is no sign of Edith's list

		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy a peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

#Francis starts a new list by entering a new item. He is less interesting than edith...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
#Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

# Again, there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

	def test_layout_and_styling(self):
		#edith goes to the home page
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)

		#she noticies the input box is necely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
			512, delta=5)

		#she starts a new list and sees the input is nicely centered there too
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/ 2,
		 512, delta=5)

if __name__ == '__main__':
	unittest.main(warnings = 'ignore')