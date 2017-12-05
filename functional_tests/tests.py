#! /usr/bin/env python3
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

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
        time.sleep(0.5)

        current_usr_one_url = self.browser.current_url
        self.assertRegex(current_usr_one_url, '/lists/.+')
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
        time.sleep(0.5)

        current_usr_two_url = self.browser.current_url
        self.assertRegex(current_usr_two_url, '/lists/.+')
        self.assertNotEqual(current_usr_two_url, current_usr_one_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('A list after new session', page_text)
        self.assertNotIn('A new list', page_text)

    def test_styling_and_layout(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id("input_text")
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512, delta=5
        )
