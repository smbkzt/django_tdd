import time
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_test(self):
        # User goes to the list page
        self.browser.get(self.live_server_url)

        # he accidentally inserts empty list
        self.browser.find_element_by_id("input_text").send_keys(Keys.ENTER)
        time.sleep(0.01)

        # The system answers with an error page
        # saying that he cant do that
        error = self.browser.find_element_by_css_selector(".has-error")
        self.assertEqual(error.text, "You can't have an empty list!")

        # User fixes his mistake, enters list
        # The systems saves his request
        self.browser.find_element_by_id("input_text").send_keys("Buy milk", Keys.ENTER)
        time.sleep(0.01)
        self.check_for_row_in_list_table("1: Buy milk")

        # Then he again sends empty list
        # Error gets again
        self.browser.find_element_by_id("input_text").send_keys(Keys.ENTER)
        time.sleep(0.01)
        error = self.browser.find_element_by_css_selector(".has-error")
        self.assertEqual(error.text, "You can't have an empty list!")
        self.check_for_row_in_list_table("1: Buy milk")

        self.browser.find_element_by_id("input_text").send_keys("Make tea", Keys.ENTER)
        time.sleep(0.01)
        self.check_for_row_in_list_table("1: Buy milk")
        self.check_for_row_in_list_table("2: Make tea")
