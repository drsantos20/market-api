from django.contrib.auth.models import User
from django.test import TestCase

from api.shopping.serializers import UserSerializer


class TestUserSerializer(TestCase):

    def setUp(self):

        self.aquaman_user = User.objects.create_user(username='aquaman', email='aquaman@dc.com', password='password')
        self.user_serializer = UserSerializer(instance=self.aquaman_user)

    def test_get_user_serializer(self):
        serializer_data = self.user_serializer.data

        self.assertEqual(serializer_data['email'], 'aquaman@dc.com')
