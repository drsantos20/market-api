from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.shopping.constants import ADD_PRODUCT_FOR_A_NON_EXISTING_WISH_LIST_ERROR_MESSAGE
from api.shopping.models import WishListProduct, WishList
from ..serializers import WishListProductSerializer


class WishListProductViewSet(viewsets.ReadOnlyModelViewSet,
                             mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin,
                             GenericViewSet,
                             ):

    permission_classes = (IsAuthenticated,)
    serializer_class = WishListProductSerializer

    def get_queryset(self):
        return WishListProduct.objects.select_related('product').filter(wish_list__user=self.request.user).order_by('id')

    def create(self, request, *args, **kwargs):
        wish_list_exists = WishList.objects.filter(user=self.request.user)

        if not wish_list_exists.exists():
            return Response(ADD_PRODUCT_FOR_A_NON_EXISTING_WISH_LIST_ERROR_MESSAGE,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        serializer = WishListProductSerializer(data=request.data, context={'request': request, 'api': wish_list_exists})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
