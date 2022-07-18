from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_401_UNAUTHORIZED
from . import serializers
from .models import Cart
from .serializers import CartSerializer
from .permissions import IsAuthorPermission, IsAuth


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuth, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class CartViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        qs = self.request.user
        queryset = super().get_queryset()
        if qs.is_anonymous:
            return ''
            # return Response('вы должны зарегаться', status=status.HTTP_401_UNAUTHORIZED)
        queryset = queryset.filter(user=qs)
        return queryset
