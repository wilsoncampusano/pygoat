from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitor(unittest.TestCase):

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
		
		self.browser.get('http://localhost:8000')
		
#she notice the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
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
		
#there is still a textbox iviting her to add another item. she
#enter "use peacock feathers to make fly"
#the page updates again, and now shos both item on her list
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		import time
		time.sleep(3)
		
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make fly')

		self.fail('Finish the test!!')
#edit wonder where the site will remember her list. then she sees that the site has generated a unique url
#for her --  the is son explanatory text to that reflect

#she visits that url - her to-do list is still there.
#satisfied , she goes back to sleep


if __name__=='__main__':	
	unittest.main(warnings = 'ignore')