""" This file contains all Tests about User app """
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegisterForm
from .views import redirect


class TestUser(TestCase):
    """Test all User app views"""

    def test_register_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_bad_register_view(self):
        """Test when information introduced is wrong"""
        response = self.client.post(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_logged_out_view(self):
        """When user is not logged in"""
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(redirect('login.html'))

    def test_logout_logged_in_view(self):
        """When the user is logged in"""
        user = User.objects.create(username="name")
        self.client.force_login(user)
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(redirect('index.html'))

    def test_profile_logged_out_view(self):
        """When user is not logged in"""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(redirect('login.html'))

    def test_profile_logged_in_view(self):
        """When the user is logged in"""
        user = User.objects.create(username="name")
        self.client.force_login(user)
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')


class TestUserForms(TestCase):
    """Test User app Form"""

    def test_valid_data(self):
        form = RegisterForm(data={
            'username': 'name',
            'email': 'email@gmail.com',
            'password1': 'abdcef123',
            'password2': 'abdcef123'
        })
        self.assertTrue(form.is_valid())

    def test_no_valid_data(self):
        """One error in the email given"""
        form = RegisterForm(data={
            'username': 'name',
            'email': 'emailgmail.com',
            'password1': 'abdcef123',
            'password2': 'abdcef123'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_no_data(self):
        """No data at all"""
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
