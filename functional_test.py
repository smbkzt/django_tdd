import unittest

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

        self.assertEqual(input_text.get_attribute("placeholder"), "Enter list element here")

        table = self.browser.find_element_by_id("table-list")

        rows = table.find_elements_by_tag_name("tr")
        self.assertTrue(
                any(row == "1: Buy apples" for row in rows)
            )


        # She is invited to enter a to-do item straight away

        self.fail("Finish the test!")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
