

from products.filters import ProductPriceFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Product, Comment, Category, Like, Favorites, Rating
from .serializers import (ProductSerializer, CommentSerializer,
                          CategorySerializer, LikeSerializer, FavoriteSerializer, RatingSerializer)
from .permissions import IsAuthor
from django.db.models import Q





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

    @action(['GET'], detail=True)
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user

        try:
            like = Like.objects.filter(product_id=product, author=user)
            res = not like[0].like
            if res:
                like[0].save()
            else:
                like.delete()
            message = 'Like' if like else 'Dislike'
        except IndexError:
            Like.objects.create(product_id=product.id, author=user, like=True)
            message = 'Like'
        return Response(message, status=200)

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



    # @action(methods=['GET'], detail=False)
    # def sort(self, request):
    #     filter = request.query_params.get('filter')
    #     if filter == 'A-Z':
    #         queryset = self.get_queryset().order_by('title')
    #     elif filter == 'Z-A':
    #         queryset = self.get_queryset().order_by('-title')
    #     elif filter == 'replies':
    #         maximum = 0
    #         for problem in self.get_queryset():
    #             if maximum < problem.replies.count():
    #                 maximum = problem.replies.count()
    #                 queryset = self.get_queryset().filter(id=problem.id)
    #     else:
    #         queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(request_body=CommentSerializer)
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthor]
        elif self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
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


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthor]
        elif self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()


