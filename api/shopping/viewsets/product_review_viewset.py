from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.shopping.models import ProductReview
from api.shopping.serializers.product_review_serializer import ProductReviewSerializer


class ProductReviewViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet,
                           ):

    permission_classes = (IsAuthenticated,)
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return ProductReview.objects.select_related('product').all().order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = ProductReviewSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
