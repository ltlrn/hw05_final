from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post

User = get_user_model()


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='follower',
        )

        cls.author = User.objects.create_user(
            username='following',
        )

        cls.post = Post.objects.create(
            text='Test post',
            author=cls.author
        )

    def setUp(self):
        self.follower_client = Client()
        self.follower_client.force_login(FollowTest.user)

        self.following_client = Client()
        self.following_client.force_login(FollowTest.author)

    def test_auth_client_can_follow(self):

        self.follower_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': FollowTest.author.username}
            ),
        )

        response = self.follower_client.get(reverse(
            'posts:follow_index')
        )

        author = response.context['page_obj'][0].author

        self.assertEqual(author, FollowTest.author)

    def test_auth_client_can_unfollow(self):
        self.follower_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': FollowTest.author.username}
            )
        )

        response = self.follower_client.get(
            reverse('posts:follow_index')
        )
        self.assertContains(response, FollowTest.author)
