from django.contrib.auth.models import User
from rest_framework import serializers

from api.shopping.constants import (
    USER_ALREADY_HAS_THIS_EMAIL_ERROR_MESSAGE,
    PRODUCT_ALREADY_EXISTS_IN_THIS_WISH_LIST_ERROR_MESSAGE,
    PRODUCT_SCORE_CANNOT_BE_GREATER_THAN_5_ERROR_MESSAGE,
    PRODUCT_DOES_NOT_EXISTS_ERROR_MESSAGE,
)
from api.shopping.models import Product, WishListProduct

USERNAME_IS_REQUIRED_ERROR_MESSAGE = 'Username is required'

PASSWORD_IS_REQUIRED_ERROR_MESSAGE = 'Password is required'


class UserValidator(object):

    def __call__(self, serializer_data):
        self.email = serializer_data.get('email')
        self.password = serializer_data.get('password')
        self.username = serializer_data.get('username')

        self.validate_duplicate_user_email()
        self.validate_user_password()
        self.validate_user_username()

    def validate_duplicate_user_email(self):
        user = User.objects.filter(email=self.email)
        if user.exists():
            raise serializers.ValidationError(USER_ALREADY_HAS_THIS_EMAIL_ERROR_MESSAGE.format(self.email))

    def validate_user_password(self):
        if not self.password:
            raise serializers.ValidationError(PASSWORD_IS_REQUIRED_ERROR_MESSAGE)

    def validate_user_username(self):
        if not self.username:
            raise serializers.ValidationError(USERNAME_IS_REQUIRED_ERROR_MESSAGE)


class WishListProductValidator(object):
    def __call__(self, serializer_data):
        self.product = serializer_data.get('product')

        self.validate_product_exists()
        self.validate_product_already_exists_on_wish_list()

    def validate_product_exists(self):
        product = Product.objects.filter(id=self.product['id'])

        if not product.exists():
            raise serializers.ValidationError(PRODUCT_DOES_NOT_EXISTS_ERROR_MESSAGE)

    def validate_product_already_exists_on_wish_list(self):
        wish_list_product = WishListProduct.objects.filter(product_id=self.product['id'])
        if wish_list_product.exists():
            raise serializers.ValidationError(PRODUCT_ALREADY_EXISTS_IN_THIS_WISH_LIST_ERROR_MESSAGE)


class ProductReviewValidator(object):
    def __call__(self, serializer_data):
        self.review_score = serializer_data.get('rating')

        self.validate_product_review_score()

    def validate_product_review_score(self):
        if self.review_score > 5:
            raise serializers.ValidationError(PRODUCT_SCORE_CANNOT_BE_GREATER_THAN_5_ERROR_MESSAGE)
