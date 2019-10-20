from django.db import models

from api.shopping.models import WishList, Product


class WishListProduct(models.Model):
    wish_list = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
