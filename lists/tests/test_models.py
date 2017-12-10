from django.test import LiveServerTestCase

from lists.models import Items, Lists


class ListandItemModelTest(LiveServerTestCase):

    def test_saving_and_retrieving_items_and_lists(self):
        list_ = Lists()
        list_.save()

        first_item = Items()
        first_item.text = "A first (ever) item"
        first_item.list = list_
        first_item.save()

        second_item = Items()
        second_item.list = list_
        second_item.text = "A second item"
        second_item.save()

        saved_items = Items.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual("A first (ever) item", first_item.text)
        self.assertEqual("A second item", second_saved_item.text)
        self.assertEqual(list_, first_saved_item.list)
        self.assertEqual(list_, second_saved_item.list)
