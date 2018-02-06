from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the homepage and accidentally tries to submit an empty list.
        # She hits Enter on the empty input box
        # The page refreshed, and there is an error message.
        # It says that the list items cannot be blank
        # She tries again with some text for the item, which now works.
        # Perversely, she now decides to submit a second blank list
        # She receives a similar warning on the list page
        # An she can correct it by filling some text in
        self.fail('write me!')