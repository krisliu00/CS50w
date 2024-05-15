from django.test import TestCase
from django.contrib.auth.models import User
from .models import CustomUser

class UserRegistrationTest(TestCase):
    def test_successful_registration(self):
        # Test successful user registration
        response = self.client.post('/register', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test1234',
            'password2': 'test1234',
            'custom name': 'Test User'  # Adjust field name if necessary
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists()) 

    def test_password_mismatch(self):
        # Test registration with password mismatch
        response = self.client.post('/register', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test1234',
            'password2': 'test12345',  
            'custom name': 'Test User'  # Adjust field name if necessary
        })
        self.assertEqual(response.status_code, 200)  
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists()) 

    def test_missing_custom_name(self):
        # Test registration with missing custom name (required field)
        response = self.client.post('/register', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test1234',
            'password2': 'test1234',
            # 'custom_name': 'Test User'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())  

