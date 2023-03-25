# Python standard library
import json
from typing import Any
from typing import Type

# Django imports
from django.test import TestCase
from django.db.models import QuerySet
from django.db.models import Model
from django.urls import reverse

# Django REST Framework
from rest_framework.test import APIClient
from rest_framework import status

# Instagram models
from instagram.core.models import User
from instagram.apps.users.models import Profile

# Create your tests here.
class BaseTestCase(TestCase):

    def setUp(self) -> None:
        """ Test case setup """
        self.user: Type[User] = User.objects.create(
            first_name='Test',
            last_name='User',
            username='test_user',
            email='testuser@example.com',
            password='{(MySup3r9@sSw0rd)-?=8hfdi',
            is_verified=True
        )

        self.request = APIClient()

        self.data: dict[str, str] = {
            'first_name': 'Chuck',
            'last_name': 'Berry',
            'username': 'chuckberry',
            'email': 'chuckberry@example.com',
            'password': '(My-Hy7P3rs3curep@ssw0rd)',
            'password_confirmation': '(My-Hy7P3rs3curep@ssw0rd)'
        }

    def get_queryset(self, klass: Model, *args: Any, **kwargs: Any) -> QuerySet:
        if kwargs:
            return klass.objects.filter(*args, **kwargs)

        return klass.objects.all()


class UserModelTestCase(BaseTestCase):

    def test_user_data(self) -> None:
        user = self.get_queryset(User, username='test_user').first()

        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.get_full_name(), 'Test User')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_user_permissions(self) -> None:
        user = self.get_queryset(User, username='test_user').first()

        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_verified, True)

    def test_user_profile(self) -> None:
        user = self.get_queryset(User, username='test_user').first()
        profile = Profile.objects.filter(user__username=user).first()

        self.assertEquals(user, profile.user)
        self.assertEquals('test_user', profile.user.username)


class UserEndPointsTestCase(BaseTestCase):

    def test_register_user(self) -> None:
        response = self.request.post(
            reverse('auth:auth-signup'),
            data=self.data,
            format='json'
        )
        message = 'Account has been created successfully'

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(json.loads(response.content)['message'], message)
        self.assertEquals(
            first=json.loads(response.content)['data']['username'],
            second=self.data['username']
        )
        self.assertEquals(
            first=json.loads(response.content)['data']['email'],
            second=self.data['email']
        )