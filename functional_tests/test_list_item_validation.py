from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_test(self):
        # User goes to the list page
        self.browser.get(self.live_server_url)

        # he accidentally inserts empty list
        self.browser.find_element_by_id("input_text").send_keys("\n")

        # The system answers with an error page
        # saying that he cant do that
        error = self.browser.find_element_by_css_selector(".has-error")
        self.assertEqual(error.text, "You can't have empty list to save!")

        # User fixes his mistake, enters list
        # The systems saves his request
        self.browser.find_element_by_id("input_text").send_keys("Buy milk\n")
        self.check_for_row_in_list_table("1: Buy milk")

        # Then he again sends empty list
        # Error gets again
        self.browser.find_element_by_id("input_text").send_keys("\n")
        error = self.browser.find_element_by_css_selector(".has-error")
        self.assertEqual(error.text, "You can't have empty list to save!")
        self.check_for_row_in_list_table("1: Buy milk")

        self.browser.find_element_by_id("input_text").send_keys("Make tea\n")
        self.check_for_row_in_list_table("1: Buy milk")
        self.check_for_row_in_list_table("2: Make tea")
