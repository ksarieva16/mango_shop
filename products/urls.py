from django.urls import path
from .views import ProductViewSet, CommentViewSet, CategoryViewSet, LikeViewSet, FavoritesViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet, 'list')
router.register('comments', CommentViewSet)
# router.register('image', ImageView)
router.register('category', CategoryViewSet)
router.register('favorites', FavoritesViewSet)
router.register('likes', LikeViewSet)

urlpatterns = []
urlpatterns += router.urls