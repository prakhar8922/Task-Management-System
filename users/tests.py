from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for User model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'test@example.com')

    def test_user_email_unique(self):
        """Test that email must be unique"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com',
                username='anotheruser',
                password='testpass123'
            )


class UserAPITest(TestCase):
    """Test cases for User API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post('/api/users/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'newuser@example.com')

    def test_user_registration_password_mismatch(self):
        """Test user registration with mismatched passwords"""
        self.user_data['password2'] = 'differentpass'
        response = self.client.post('/api/users/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile_requires_authentication(self):
        """Test that user profile requires authentication"""
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_retrieve(self):
        """Test retrieving user profile"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
