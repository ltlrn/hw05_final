from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()

ADDRESSES_UNAUTH = [
    '/',
    '/group/test-slug/',
    '/profile/some/',
    '/posts/1/',
    '/unexisting_page/',
]

ADDRESSES_AUTH = [
    '/posts/1/edit/',
    '/create/',
]

TEMPLATES_DICT = {
    '/': 'posts/index.html',
    '/group/test-slug/': 'posts/group_list.html',
    '/profile/some/': 'posts/profile.html',
    '/posts/1/': 'posts/post_detail.html',
    '/posts/1/edit/': 'posts/create_post.html',
    '/create/': 'posts/create_post.html',
}


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='some')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug='test-slug'
        )

        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    def test_urls_exists_at_desired_locations(self):
        """Доступность страниц приложения posts по ожидаемым адресам."""

        for address in ADDRESSES_UNAUTH:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                current_code = HTTPStatus.OK
                if address == '/unexisting_page/':
                    current_code = HTTPStatus.NOT_FOUND
                self.assertEqual(response.status_code, current_code)

    def test_urls_exists_for_authorized_users(self):
        """Доступность страниц для авторизованных пользователей."""

        for address in ADDRESSES_AUTH:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)

                if address == '/posts/1/edit/':
                    self.assertEqual(
                        PostURLTests.user,
                        PostURLTests.post.author
                    )

                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_anonymous(self):
        """Проверка перенаправления неавторизованных пользователей."""

        for address in ADDRESSES_AUTH:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                redirect_to = '/auth/login/'
                self.assertRedirects(
                    response, (f'{redirect_to}?next={address}')
                )

    def test_urls_use_correct_templates(self):
        """Проверка соответствия шаблонов страниц их адресам."""

        for address, template in TEMPLATES_DICT.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
