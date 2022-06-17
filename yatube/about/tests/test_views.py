from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

PAGE_NAMES_TEMPLATES = {
    reverse('about:author'): 'about/author.html',
    reverse('about:tech'): 'about/tech.html',
}


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_pages_accessible_by_name(self):
        """URL, генерируемыe при помощи имен, доступны."""

        for reverse_name in PAGE_NAMES_TEMPLATES:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_pages_uses_correct_template(self):
        """При запросе к именам применяются верные шаблоны."""

        for reverse_name, template in PAGE_NAMES_TEMPLATES.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
