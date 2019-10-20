from django.contrib.auth.models import User
from django.test import TestCase

from api.shopping.models import Customer
from api.shopping.serializers import CustomerSerializer


class TestCustomerSerializer(TestCase):

    def setUp(self):
        self.aquaman_user = User.objects.create_user(username='aquaman', email='aquaman@dc.com', password='password')
        self.aquaman_customer = Customer.objects.create(name='aquaman', user=self.aquaman_user)

        self.user_serializer = CustomerSerializer(instance=self.aquaman_customer)

    def test_get_customer_serializer(self):
        serializer_data = self.user_serializer.data
        self.assertEqual(serializer_data['name'], 'aquaman')
