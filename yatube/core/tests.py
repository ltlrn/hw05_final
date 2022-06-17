from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page(self):
        """Проверка статуса ответа и используемого шаблона."""

        response = self.client.get('/nonexist-page/')

        with self.subTest():
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, 'core/404.html')
