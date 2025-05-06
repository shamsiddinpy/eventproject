# authentication/tests.py
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticationTests(APITestCase):
    def setUp(self):
        # Create a test user for login tests
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpassword123'
        )

        # Registration data
        self.register_data = {
            'username': 'newuser',
            'email': 'newuser@gmail.com',
            'password': 'newuserpassword123',
            'password2': 'newuserpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }

        # Login data
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }

    def test_user_registration(self):
        """Test user registration endpoint"""
        url = reverse('auth_register')
        response = self.client.post(url, self.register_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='newuser').email, 'newuser@gmail.com')

    def test_user_login(self):
        """Test user login and token generation endpoint"""
        url = reverse('token_obtain_pair')
        response = self.client.post(url, self.login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_token_refresh(self):
        """Test token refresh endpoint"""
        # Get a refresh token
        refresh = RefreshToken.for_user(self.test_user)

        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': str(refresh)}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_registration_with_mismatched_passwords(self):
        """Test registration fails with mismatched passwords"""
        data = self.register_data.copy()
        data['password2'] = 'differentpassword'

        url = reverse('auth_register')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_with_existing_username(self):
        """Test registration fails with existing username"""
        data = self.register_data.copy()
        data['username'] = 'testuser'  # Already exists

        url = reverse('auth_register')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
