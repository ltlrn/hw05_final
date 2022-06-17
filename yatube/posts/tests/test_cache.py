from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post

User = get_user_model()


class CacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='test_user')

        Post.objects.create(
            author=cls.user,
            text='text_first'
        )

        Post.objects.create(
            author=cls.user,
            text='text_second'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(CacheTest.user)

    def test_cache_index(self):
        """Cache work in index."""

        post_count = Post.objects.count()
        response = self.authorized_client.get(
            reverse('posts:main_page')
        )

        Post.objects.first().delete()

        self.assertEqual(post_count, len(response.context['page_obj']))
        cache.clear()
        self.assertEqual(post_count, Post.objects.count() + 1)
