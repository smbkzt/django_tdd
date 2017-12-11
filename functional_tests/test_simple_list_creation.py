import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To Do List', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("To-Do", header_text)

        input_text = self.browser.find_element_by_id("input_text")
        self.assertEqual(input_text.get_attribute("placeholder"),
                         "Enter a to-do item")
        input_text.send_keys("A new list")
        input_text.send_keys(Keys.ENTER)
        time.sleep(0.2)

        current_usr_one_url = self.browser.current_url
        self.assertRegex(current_usr_one_url, '/lists/.+')
        time.sleep(0.2)
        self.check_for_row_in_list_table("1: A new list")

        # We want to check whether the another user dont
        # see the prev user's data (sessions)
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("1: A new list", body)

        input_box = self.browser.find_element_by_id("input_text")
        input_box.send_keys("A list after new session")
        input_box.send_keys(Keys.ENTER)
        time.sleep(0.2)

        current_usr_two_url = self.browser.current_url
        self.assertRegex(current_usr_two_url, '/lists/.+')
        self.assertNotEqual(current_usr_two_url, current_usr_one_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('A list after new session', page_text)
        self.assertNotIn('A new list', page_text)
