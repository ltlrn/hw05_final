from http import HTTPStatus

from django.test import Client, TestCase

ADDRESSES = [
    '/about/author/',
    '/about/tech/',
]

TEMPLATES_DICT = {
    '/about/author/': 'about/author.html',
    '/about/tech/': 'about/tech.html',
}


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_exist_at_desired_locations(self):
        """Доступность страниц приложения about по ожидаемым адресам."""

        for address in ADDRESSES:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_use_correct_templates(self):
        """Проверка соответствия шаблонов страниц их адресам."""

        for address, template in TEMPLATES_DICT.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
