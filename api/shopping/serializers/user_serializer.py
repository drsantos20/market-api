from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from api.shopping.models import Customer
from api.shopping.validators import UserValidator


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'customer', 'username', 'password')

        validators = [
            UserValidator()
        ]

    @transaction.atomic
    def create(self, validated_data):
        customer_data = validated_data.pop('customer')

        user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'], password=validated_data['password'])
        customer, created = Customer.objects.update_or_create(user=user, name=customer_data['name'])

        return customer

    def update(self, instance, validated_data):
        instance.customer.name = validated_data['customer']['name']
        instance.customer.save()
        return instance.customer
