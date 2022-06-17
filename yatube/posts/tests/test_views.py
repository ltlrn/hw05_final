import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post
from .utils_for_testing import create_test_dicts_list

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

PAGE_NAMES_TEMPLATES = {
    reverse('posts:main_page'): 'posts/index.html',
    reverse('posts:group_list', kwargs={
        'slug': 'test-slug'
    }): 'posts/group_list.html',
    reverse('posts:profile', kwargs={
        'username': 'some_user'
    }): 'posts/profile.html',
    reverse('posts:post_detail', kwargs={
        'post_id': 1
    }): 'posts/post_detail.html',
    reverse('posts:post_edit', kwargs={
        'post_id': 1
    }): 'posts/create_post.html',
    reverse('posts:post_create'): 'posts/create_post.html',
}

TEST_DICTS = create_test_dicts_list(
    names_list=list(PAGE_NAMES_TEMPLATES.keys())[:3],
    number_of_posts=13,
    posts_per_page=10,
)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

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

        cls.user = User.objects.create_user(username='some_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug='test-slug'
        )

        cls.post_objects = []

        for record in range(1, 14):
            cls.post_objects.append(
                Post(
                    author=cls.user,
                    group=cls.group,
                    text=f'Тестовый текст {record}',
                    image=uploaded
                )
            )

        Post.objects.bulk_create(cls.post_objects)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsViewsTest.user)

    def test_pages_using_correct_template(self):
        """URL адреса используют соответствующие шаблоны."""

        for reverse_name, template in PAGE_NAMES_TEMPLATES.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_with_paginator(self):
        """Проверка паджинации главной страницы, страницы группы и профиля."""

        for test_dict in TEST_DICTS:
            for reverse_name, pages in zip(test_dict, test_dict.values()):
                with self.subTest(reverse_name=reverse_name):
                    response = self.authorized_client.get(reverse_name)
                    self.assertEqual(len(response.context['page_obj']), pages)

    def test_context_of_pages_without_forms(self):
        """Проверка контекста страниц, не содержащих веб-форму."""

        page_objects = [
            Post.objects.all()[:10],
            Post.objects.filter(group=self.group)[:10],
            Post.objects.filter(author=self.user)[:10],
            'post',
        ]

        for reverse_name, page in zip(
            list(PAGE_NAMES_TEMPLATES.keys())[:4],
            page_objects
        ):

            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                if page == 'post':
                    self.assertEqual(
                        response.context.get(page).text,
                        'Тестовый текст 1'
                    )

                    self.assertTrue(
                        response.context.get(page).image
                    )

                else:
                    self.assertEqual(
                        response.context.get('page_obj').object_list,
                        list(page)
                    )

                    self.assertTrue(
                        response.context.get('page_obj').object_list[0].image
                    )

    def test_context_of_pages_with_forms(self):
        """Проверка котекста страниц с веб-формами."""

        for reverse_name in list(PAGE_NAMES_TEMPLATES.keys())[4:]:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                form_fields = {
                    'text': forms.CharField,
                    'group': forms.ChoiceField,
                }

                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get(
                            'form'
                        ).fields.get(value)
                        self.assertIsInstance(form_field, expected)
