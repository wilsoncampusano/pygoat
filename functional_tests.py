from selenium import webdriver
import unittest

class NewVisitor(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrive_it_latter(self):

#edit has hear about a cool new online to-do app. she goes
#to check out its homepage
		
		self.browser.get('http://localhost:8000')
		
#she notice the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!!')
#she is invited to enter a to-do item straight away

#she types "buy peacock feathers" into a textbox(edith's hoby is tying fly-fishing lures)
#when hits enter, the page updates, an now the page lists
# 1: Buy a peacock feathers as an item in a to-do list
#there is still a textbox iviting her to add another item. she
#enter "use peacock feathers to make fly"
#the page updates again, and now shos both item on her list
#edit wonder where the site will remember her list. then she sees that the site has generated a unique url
#for her --  the is son explanatory text to that reflect

#she visits that url - her to-do list is still there.
#satisfied , she goes back to sleep
if __name__=='__main__':
	unittest.main(warnings = 'ignore')