from django.contrib.auth.models import User
from rest_framework import serializers

from api.shopping.models import WishList


class WishListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = WishList
        fields = ('name',)

    def create(self, validated_data):
        user = self.context['request'].user
        user = User.objects.get(
            email=user.email
        )

        wish_list = WishList.objects.create(
            user=user,
            name=validated_data['name']
        )

        wish_list.save()
        return wish_list
