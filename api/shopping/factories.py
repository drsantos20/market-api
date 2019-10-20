import factory
import random

from django.contrib.auth.models import User

from api.shopping.models import Product, ProductReview, Customer, WishList, WishListProduct


class ProductFactory(factory.DjangoModelFactory):
    title = factory.Faker('pystr')
    brand = factory.Faker('pystr')
    price = factory.Faker('random_int')
    image = factory.Faker('pystr')

    class Meta:
        model = Product


class ProductReviewFactory(factory.DjangoModelFactory):
    review_title = factory.Faker('pystr')
    review_text = factory.Faker('pystr')
    rating = random.randint(1, 5)
    product = factory.SubFactory(ProductFactory)

    class Meta:
        model = ProductReview


class UserFactory(factory.DjangoModelFactory):
    email = factory.Faker('pystr')
    username = factory.Faker('pystr')

    class Meta:
        model = User


class CustomerFactory(factory.DjangoModelFactory):
    name = factory.Faker('pystr')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Customer


class WishListFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('pystr')

    class Meta:
        model = WishList


class WishListProductFactory(factory.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    wish_list = factory.SubFactory(WishListFactory)

    class Meta:
        model = WishListProduct
