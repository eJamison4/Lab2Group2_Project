from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from django.urls import reverse

User = get_user_model()

class LogoutUnitTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            userEmail='test@example.com',
            firstName='Test',
            lastName='User',
            homeAddress='123 Main St',
            phoneNumber='5551234567',
            accountType=0
        )

    def test_logout_view_redirects_authenticated_user(self):
        """Test that logout view logs out a user and redirects to login page"""
        request = self.factory.get(reverse('logout'))
        request.user = self.user

        response = LogoutView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_logout_view_redirects_anonymous_user(self):
        """Test that logout view still redirects anonymous users to login"""
        request = self.factory.get(reverse('logout'))
        request.user = AnonymousUser()

        response = LogoutView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
