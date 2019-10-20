from rest_framework import serializers

from api.shopping.models import Product
from api.shopping.serializers.product_review_serializer import ProductReviewSerializer


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    brand = serializers.CharField(required=False)
    reviewScore = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(required=False)
    image = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)
    product_review = ProductReviewSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'brand',
            'reviewScore',
            'price',
            'image',
            'product_review',
        )
