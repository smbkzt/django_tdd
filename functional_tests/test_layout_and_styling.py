from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_styling_and_layout(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id("input_text")
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512, delta=5
        )
