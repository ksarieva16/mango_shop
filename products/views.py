from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     RetrieveAPIView, UpdateAPIView,
                                     DestroyAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Product, Comment, Category, Like, Favorites
from .serializers import (ProductSerializer, CommentSerializer,
                          CategorySerializer,
                          LikeSerializer, FavoriteSerializer)
from .permissions import IsAuthor

from products.filters import ProductPriceFilter


@swagger_auto_schema(request_body=ProductSerializer)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
    filterset_class = ProductPriceFilter
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        product = self.get_object()
        obj, created = Like.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.like = not obj.like
            obj.save()
        liked_or_unliked = 'liked' if obj.like else 'unliked'
        return Response('Successfully {} product'.format(liked_or_unliked), status=status.HTTP_200_OK)

    @action(['GET'], detail=True)
    def favorite(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            favorites = Favorites.objects.filter(product_id=product, author=user)
            res = not favorites[0].favorites
            if res:
                favorites[0].save()
            else:
                favorites.delete()
            message = 'In favorites' if favorites else 'Not in favorites'
        except IndexError:
            Favorites.objects.create(product_id=product.id, author=user, favorites=True)
            message = 'In favorites'
        return Response(message, status=200)



class CreateProductView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailsView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@swagger_auto_schema(request_body=CommentSerializer)
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()



@swagger_auto_schema(request_body=CategorySerializer)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


# @swagger_auto_schema(request_body=ProductSerializer)
# class LikeViewSet(ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#
#
# @swagger_auto_schema(request_body=ProductSerializer)
# class FavoritesViewSet(ModelViewSet):
#     queryset = Favorites.objects.all()
#     serializer_class = FavoriteSerializer