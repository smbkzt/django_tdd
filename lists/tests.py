import time

from django.template.loader import render_to_string
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from .models import Items


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Items()
        first_item.text = "A first (ever) item"
        first_item.save()

        second_item = Items()
        second_item.text = "A second item"
        second_item.save()

        saved_items = Items.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(first_item, saved_items[0])
        self.assertEqual(second_item, saved_items[1])


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Items.objects.create(text="Itemss1")
        Items.objects.create(text="Itemss2")

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'Itemss1')
        self.assertContains(response, 'Itemss2')


class NewListTest(TestCase):

    def test_home_page_can_save_a_post_requests(self):
        self.client.post(
            '/list/new/',
            data={"item_text": "A new list"}
        )

        # self.assertEqual(Items.objects.all().count(), 1)
        # first_item = Items.objects.first().text
        # self.assertEqual(first_item, "A new list")

    def test_redirects_after_post_request(self):
        response = self.client.post(
            '/lists/new/',
            data={'item_text': 'A new list item'}
        )
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
