from .views import ProductViewSet, CommentViewSet, CategoryViewSet, RatingViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet, 'list')
router.register('comments', CommentViewSet)
# router.register('image', ImageView)
router.register('category', CategoryViewSet)
# router.register('favorites', FavoriteViewSet)
# router.register('likes', LikeViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = []
urlpatterns += router.urls