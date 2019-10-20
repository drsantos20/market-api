from django.contrib.auth.models import User
from django.test import TestCase


class UserTestCase(TestCase):

    def setUp(self):
        self.aquaman_user = User.objects.create_user(username='aquaman', email='aquaman@dc.com', password='password')
        self.superman_user = User.objects.create_user(username='superman', email='superman@dc.com', password='password')

    def test_get_user(self):
        user_a = User.objects.get(username='aquaman')
        user_b = User.objects.get(username='superman')
        self.assertEqual(user_a.username, self.aquaman_user.username)
        self.assertEqual(user_b.username, self.superman_user.username)
