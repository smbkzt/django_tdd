from unittest import skip

from django.utils.html import escape
from django.urls import resolve
from django.test import TestCase

from lists.views import home_page
from lists.models import Items, Lists


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = Lists.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        needed_list = Lists.objects.create()
        Items.objects.create(text="Needed item1", list=needed_list)
        Items.objects.create(text="Needed item2", list=needed_list)

        fake_list = Lists.objects.create()
        Items.objects.create(text="Fake item1", list=fake_list)
        Items.objects.create(text="Fake item1", list=fake_list)

        response = self.client.get('/lists/%d/' % (needed_list.id))

        self.assertContains(response, 'Needed item1')
        self.assertContains(response, 'Needed item2')

        self.assertNotContains(response, 'Fake item1')
        self.assertNotContains(response, 'Fake item2')

    @skip
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ""})

        expected_error = escape("You can't have an empty list!")
        self.assertContains(response, expected_error)

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = Lists.objects.create()
        response = self.client.post(
            '/lists/%d/' % (list_.id),
            data={'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list!")
        self.assertContains(response, expected_error)

    def test_home_page_can_save_a_post_requests_to_an_existing_list(self):
        other_list_ = Lists.objects.create()
        correct_list = Lists.objects.create()
        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={"item_text": "A new list"}
        )

        self.assertEqual(Items.objects.count(), 1)
        first_item = Items.objects.first()
        self.assertEqual(first_item.text, "A new list")
        self.assertEqual(first_item.list, correct_list)

    def test_redirects_after_post_request(self):
        other_list = Lists.objects.create()
        correct_list = Lists.objects.create()

        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'item_text': 'A new list item'}
        )
        self.assertRedirects(
            response, '/lists/%d/' % (correct_list.id)
        )

    def test_dint_save_invalid_items(self):
        self.client.post('/lists/new', data={'input_text': ""})
        self.assertEqual(Items.objects.count(), 0)
        self.assertEqual(Lists.objects.count(), 0)

    def test_passes_correct_list_to_the_template(self):
        correct_list = Lists.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context["list"], correct_list)
