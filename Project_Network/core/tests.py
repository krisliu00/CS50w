from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_can_register(self):
        # Prepare registration form data
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'customname': 'Test User',
            'bio': 'This is a test bio.',
            'age': 25,
            'password': 'password123',
            'confirmation': 'password123',
        }

        # Simulate user registration
        response = self.client.post(reverse('core:register'), data)

        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Verify that the user is created
        user = get_user_model().objects.filter(username=data['username']).first()
        self.assertTrue(user is not None)
        self.assertTrue(user.check_password(data['password']))
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.custom_name, data['customname'])
        self.assertEqual(user.bio, data['bio'])
        self.assertEqual(user.age, data['age'])

        # Ensure no duplicate username is created
        self.assertRaises(ValueError, get_user_model().objects.create_user, **data)
