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

    def test_home_page_return_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html", request=request)

        # The same problem with tokens
        # self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_post_requests(self):
        request = HttpRequest()
        request.method == 'POST'
        request.POST['item_text'] = "A new list item"

        response = home_page(request)
        new_resp = home_page(HttpRequest())
        # Cuz the home page redirects to '/'

        new_item_text = Items.objects.first().text

        self.assertEqual(Items.objects.all().count(), 1)
        self.assertEqual(new_item_text, "A new list item")

        self.assertIn("A new list item", new_resp.content.decode())

        expected_html = render_to_string(
            'home.html',
            {"all_items": Items.objects.all()},
            request=request
        )

        # Tokens are not equal
        # self.assertEqual(response.content.decode(), expected_html)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_page_saves_object_when_its_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Items.objects.count(), 0)

    def test_page_displays_all_the_list(self):
        Items.objects.create(text="Item1")
        Items.objects.create(text="Item2")

        request = HttpRequest()
        response = home_page(request)

        self.assertIn("Item1", response.content.decode())
        self.assertIn("Item2", response.content.decode())


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
