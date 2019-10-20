from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum


class Product(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False, unique=True)
    brand = models.CharField(max_length=150, null=False, blank=False)
    reviewScore = models.IntegerField(default=0)
    price = models.IntegerField(null=False, blank=False)
    image = models.URLField(
        max_length=2000,
        null=True,
        blank=True,
    )


@receiver(post_save, sender='shopping.ProductReview')
def update_product_review_score(sender, instance, created, **kwargs):
    from api.shopping.models import ProductReview
    if created:
        sum_rating_score_from_product = ProductReview.objects.filter(product_id=instance.product_id).aggregate(Sum('rating'))
        total_of_reviews_from_product = ProductReview.objects.filter(product_id=instance.product_id)

        rating_score = sum_rating_score_from_product['rating__sum'] / total_of_reviews_from_product.count()
        product = Product.objects.get(id=instance.product_id)
        product.reviewScore = rating_score
        product.save()
