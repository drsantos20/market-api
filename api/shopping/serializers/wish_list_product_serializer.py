from rest_framework import serializers

from api.shopping.models import Product
from api.shopping.models.wish_list_product import WishListProduct
from api.shopping.serializers.product_serializer import ProductSerializer
from api.shopping.serializers.wish_list_serializer import WishListSerializer
from api.shopping.validators import WishListProductValidator


class WishListProductSerializer(serializers.ModelSerializer):
    wish_list = WishListSerializer(required=False)
    product = ProductSerializer(required=True)

    class Meta:
        model = WishListProduct
        fields = ('wish_list', 'product',)

        validators = [
            WishListProductValidator()
        ]

    def create(self, validated_data):
        wish_list_product_from_user = self.context['api'].first()

        product = Product.objects.get(
            id=validated_data['product']['id'],
        )

        add_new_product_to_user_wish_list = WishListProduct.objects.create(
            wish_list=wish_list_product_from_user,
            product=product
        )

        add_new_product_to_user_wish_list.save()

        return add_new_product_to_user_wish_list
