from django.contrib.auth.models import User
from django.test import TestCase

from api.shopping.models import Customer


class CustomerTestCase(TestCase):

    def setUp(self):
        self.aquaman_user = User.objects.create_user(username='aquaman', email='aquaman@dc.com', password='password')
        self.superman_user = User.objects.create_user(username='superman', email='superman@dc.com', password='password')

        self.aquaman = Customer.objects.create(name='aquaman', user=self.aquaman_user)
        self.superman = Customer.objects.create(name='superman', user=self.superman_user)

    def test_get_customer(self):
        user_a = Customer.objects.get(name='aquaman')
        user_b = Customer.objects.get(name='superman')
        self.assertEqual(user_a.name, self.aquaman.name)
        self.assertEqual(user_b.name, self.superman.name)
