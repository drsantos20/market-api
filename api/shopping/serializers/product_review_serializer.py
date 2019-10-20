from rest_framework import serializers

from api.shopping.models import ProductReview, Product
from api.shopping.validators import ProductReviewValidator


class ProductReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    review_title = serializers.CharField(required=True)
    review_text = serializers.CharField(required=True)
    rating = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)

    class Meta:
        model = ProductReview
        fields = (
            'id',
            'review_title',
            'review_text',
            'rating',
            'product_id',
        )

    validators = [
        ProductReviewValidator()
    ]

    def create(self, validated_data):
        product = Product.objects.get(
            id=validated_data['product_id']
        )

        validated_data.pop('product_id')
        product_review = ProductReview.objects.create(**validated_data, product=product)

        return product_review
