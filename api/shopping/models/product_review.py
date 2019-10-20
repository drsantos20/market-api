from django.db import models

from api.shopping.models import Product


class ProductReview(models.Model):
    review_title = models.CharField(max_length=150, null=False, blank=False, unique=False)
    review_text = models.CharField(max_length=150, null=False, blank=False)

    VERY_BAD = 1
    BAD = 2
    NEUTRAL = 3
    GOOD = 4
    VERY_GOOD = 5

    RATING_CHOICES = (
        (VERY_BAD, 'Very Bad'),
        (BAD, 'Bad'),
        (NEUTRAL, 'Neutral'),
        (GOOD, 'Good'),
        (VERY_GOOD, 'Very Good'),
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=VERY_BAD,
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
