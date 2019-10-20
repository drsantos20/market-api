from django.contrib.auth.models import User
from django.test import TestCase

from api.shopping.models import WishList


class WishListTestCase(TestCase):
    def setUp(self):
        self.aquaman_user = User.objects.create_user(username='aquaman', email='aquaman@dc.com', password='password')
        self.santa_claus_wish_list = WishList.objects.create(name='santa_claus_wish_list', user=self.aquaman_user)

    def test_create_wish_list(self):
        wish_list = WishList.objects.get(name='santa_claus_wish_list')
        self.assertEqual(wish_list.name, self.santa_claus_wish_list.name)
