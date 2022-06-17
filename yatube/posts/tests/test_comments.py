from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Comment, Post

User = get_user_model()


class CommentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_1 = User.objects.create_user(username='test_user_1')
        cls.user_2 = User.objects.create_user(username='test_user_2')

        cls.post = Post.objects.create(
            text='Test text',
            author=cls.user_1
        )

        cls.comment = Comment.objects.create(
            author=cls.user_2,
            post=cls.post,
            text='This post is awesome!'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(CommentTest.user_2)

    def test_add_comments(self):
        """Тест добавления комментариев."""

        comments_count = Comment.objects.count()

        form_data = {'text': CommentTest.comment.text}

        response = self.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': CommentTest.post.id}
            ),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': CommentTest.post.id}
            )
        )

        self.assertEqual(Comment.objects.count(), comments_count + 1)

        self.assertTrue(
            Comment.objects.filter(author=CommentTest.user_2).exists()
        )
