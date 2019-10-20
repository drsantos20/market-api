from django.contrib.auth.models import User
from django.db import models


class WishList(models.Model):
    name = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name='wish_lists')

