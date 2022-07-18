
from rest_framework.viewsets import ModelViewSet

from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Product, Comment, Image, Category, Like, Favorites
from .serializers import (ProductSerializer, CommentSerializer,
                          ImageSerializer,  CategorySerializer,
                          LikeSerializer, FavoritesSerializer)
from .permissions import IsAuthor

from products.filters import ProductPriceFilter


@swagger_auto_schema(request_body=ProductSerializer)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    filterset_class = ProductPriceFilter

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


@swagger_auto_schema(request_body=CommentSerializer)
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()


@swagger_auto_schema(request_body=ImageSerializer)
class ImageView(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [permissions.IsAdminUser]
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


@swagger_auto_schema(request_body=ProductSerializer)
class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


@swagger_auto_schema(request_body=ProductSerializer)
class FavoritesViewSet(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer

