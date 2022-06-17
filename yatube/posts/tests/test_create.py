from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

PAGE_NAMES = [
    reverse('posts:main_page'),
    reverse('posts:group_list', kwargs={
        'slug': 'test-slug3'
    }),
    reverse('posts:profile', kwargs={
        'username': 'some_user'
    }),
    reverse('posts:group_list', kwargs={
        'slug': 'test-slug2'
    })
]

User = get_user_model()


class PostCreateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='some_user')

        cls.group_objects = []

        for record in range(1, 4):
            cls.group_objects.append(
                Group(
                    pk=record,
                    title=f'Тестовая группа {record}',
                    slug=f'test-slug{record}',
                )
            )

        cls.groups = Group.objects.bulk_create(cls.group_objects)

        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.groups[-1],
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateTest.user)

    def test_appearence(self):
        """
        Проверка появления новой публикации на главной странице,
        странице профиля, странице группы.
        """

        for test_number, address in enumerate(PAGE_NAMES):
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                if test_number == 3:
                    self.assertFalse(
                        response.context.get('page_obj').object_list
                    )
                else:
                    if test_number == 0:
                        value = response.context.get(
                            'page_obj'
                        ).object_list[0].group.title

                        expected = 'Тестовая группа 3'

                    elif test_number == 1:
                        value = response.context.get(
                            'page_obj'
                        ).object_list[0].group.title

                        expected = response.context.get('group').title

                    elif test_number == 2:
                        value = response.context.get('posts')[0].group.title
                        expected = response.context.get(
                            'author'
                        ).posts.all()[0].group.title

                    self.assertEqual(value, expected)
