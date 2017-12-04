import unittest
import time


from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To Do List', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("To-Do", header_text)

        input_text = self.browser.find_element_by_id("input-text")
        self.assertEqual(input_text.get_attribute("placeholder"),
                         "Enter list element here")
        input_text.send_keys("A new list")
        input_text.send_keys(Keys.ENTER)

        time.sleep(1)

        self.check_for_row_in_list_table("1: A new list")

        self.fail("Finish the test!")

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("table-list")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])


if __name__ == '__main__':
    unittest.main(warnings='ignore')
