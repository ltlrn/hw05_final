import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='some_user')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug='test-slug',
        )

        cls.group_2 = Group.objects.create(
            title='Другая группа',
            description='Тестовое описание',
            slug='test-slug2'
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTest.user)

    def test_create_post(self):
        """Тест формы создания публикации."""

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/bmp'
        )

        posts_count = Post.objects.count()

        form_data = {
            'text': 'Тестовый текст',
            'group.title': PostFormTest.group,
            'image': uploaded,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse(
                'posts:profile',
                kwargs={'username': 'some_user'}
            )
        )

        self.assertEqual(Post.objects.count(), posts_count + 1)

        self.assertTrue(
            'TEMP_MEDIA_ROOT/small.gif'
        )

    def test_edit_post(self):
        """Тест формы редактирования публикации."""

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/bmp'
        )

        form_data = {
            'text': 'Отредактированный текст',
            'group.title': PostFormTest.group_2,
            'image': uploaded,
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': 1}),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': 1}
            )
        )

        with self.subTest():
            self.assertEqual(
                Post.objects.filter(id=1)[0].text,
                form_data['text'],
            )

            self.assertEqual(
                Group.objects.filter(title=form_data['group.title'])[0].title,
                form_data['group.title'].title
            )
