from django.test import LiveServerTestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Items, Lists


class HomePageTest(LiveServerTestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(LiveServerTestCase):

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


class NewListTest(LiveServerTestCase):

    def test_passes_correct_list_to_the_template(self):
        correct_list = Lists.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context["list"], correct_list)

    def test_home_page_can_save_a_post_requests_to_an_existing_list(self):
        pass
        # list_ = Lists.objects.create()

        # self.client.post(
        #     '/list/%d/add_item' % (list_.id,),
        #     data={"item_text": "A new list"}
        # )
        # self.assertEqual(Items.objects.all().count(), 1)
        # first_item = Items.objects.first().text
        # self.assertEqual(first_item, "A new list")

    def test_redirects_after_post_request(self):
        list_ = Lists.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (list_.id,),
            data={'item_text': 'A new list item'}
        )
        self.assertRedirects(
            response, '/lists/%d/' % (list_.id)
        )
