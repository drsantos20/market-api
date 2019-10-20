from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.shopping.models import Product
from api.shopping.serializers.product_serializer import ProductSerializer


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet,
                     mixins.DestroyModelMixin,
                     ):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
