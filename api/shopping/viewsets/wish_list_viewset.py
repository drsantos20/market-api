from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.shopping.constants import (
    CREATE_WISH_LIST_FOR_USER_THAT_ALREADY_HAVE_WISH_LIST_ERROR_MESSAGE,
)
from api.shopping.models import WishList
from api.shopping.serializers.wish_list_serializer import WishListSerializer


class WishListViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet,
                      ):

    permission_classes = (IsAuthenticated,)
    serializer_class = WishListSerializer

    def get_queryset(self):
        return WishList.objects.select_related('user').filter(user=self.request.user).order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = WishListSerializer(data=request.data, context={'request': request})

        wish_list = WishList.objects.filter(user=self.request.user)

        if wish_list.exists():
            return Response(CREATE_WISH_LIST_FOR_USER_THAT_ALREADY_HAVE_WISH_LIST_ERROR_MESSAGE,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
