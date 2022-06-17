from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='some_user')

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

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelCase.post
        group = PostModelCase.group

        printable_output = {
            post: post.text[:15],
            group: group.title,
        }

        for value, expected in printable_output.items():
            with self.subTest(value=value):
                self.assertEqual(
                    str(value),
                    expected,
                    'Не выводится нужный __str__',
                )

    def test_label_verboses(self):

        post_fields_verboses = [
            ('text', 'Текст публикации'),
            ('pub_date', 'Дата публикации'),
            ('author', 'Автор'),
            ('group', 'Сообщество'),
        ]

        group_fields_verboses = [
            ('title', 'Название группы'),
            ('description', 'Описание группы'),
        ]

        models = {
            PostModelCase.post: post_fields_verboses,
            PostModelCase.group: group_fields_verboses,
        }

        for current_model in models:
            for field, expected in models[current_model]:
                with self.subTest(field=field):

                    verbose = current_model._meta.get_field(field).verbose_name
                    self.assertEqual(verbose, expected)
