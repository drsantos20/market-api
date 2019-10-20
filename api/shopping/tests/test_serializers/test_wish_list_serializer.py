from django.contrib.auth.models import User
from django.test import TestCase

from api.shopping.models import WishList
from api.shopping.serializers.wish_list_serializer import WishListSerializer


class TestWishlistSerializer(TestCase):
    def setUp(self):

        self.aquaman_user = User.objects.create_user(username='aquaman', email='aquaman@dc.com', password='password')
        self.santa_claus_wish_list = WishList.objects.create(name='santa_claus_wish_list', user=self.aquaman_user)

        self.wish_list_product_serializer = WishListSerializer(instance=self.santa_claus_wish_list)

    def test_get_wish_list_serializer(self):

        serializer_data = self.wish_list_product_serializer.data
        self.assertEqual(serializer_data['name'], 'santa_claus_wish_list')
