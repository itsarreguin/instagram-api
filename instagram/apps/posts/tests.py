# Django imports
from django.urls import reverse

# instagram tests
from instagram.apps.accounts.tests import BaseTestCase
# Instagram models
from instagram.core.models import User
from instagram.apps.posts.models import Post


class PostTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        Post.objects.create(author=self.user, image='image.png', description='My first post')
        Post.objects.create(author=self.user, image='another_img.png', description='Second Post')


class PostModelTestCase(PostTestCase):

    def test_create_post(self) -> None:
        user = self.get_queryset(User, username='test_user').first()
        post = self.get_queryset(Post, author__username=user).first()

        self.assertEquals(post.author, user)
        self.assertEquals(post.image.name, 'image.png')
        self.assertIsInstance(post, Post)

    def test_update_post(self) -> None:
        post = self.get_queryset(Post, author__username='test_user').first()
        post.description = 'This is anoter description'
        post.save()

        post2 = self.get_queryset(Post, author__username='test_user').last()
        post2.description = 'Description changed'
        post2.save()

        self.assertEquals(post.description, 'This is anoter description')
        self.assertEquals(post2.description, 'Description changed')

    def test_total_posts(self) -> None:
        posts = self.get_queryset(Post)

        self.assertEquals(posts.count(), 2)
        self.assertCountEqual(posts, posts)