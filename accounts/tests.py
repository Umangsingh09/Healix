from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserProfile

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.token_refresh_url = '/api/auth/token/refresh/'

    def test_user_registration(self):
        """Test user registration with profile creation"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'patient',
            'phone': '1234567890',
            'address': '123 Test St'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Check user and profile were created
        user = User.objects.get(username='testuser')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.role, 'patient')
        self.assertEqual(profile.phone, '1234567890')

    def test_user_login(self):
        """Test user login"""
        # Create user first
        user = User.objects.create_user(username='testuser', password='testpass123')
        UserProfile.objects.create(user=user, role='patient')

        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
