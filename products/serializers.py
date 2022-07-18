from rest_framework import serializers
from multiprocessing import context
from products.models import Product, ProductReview, Comment, Category, Like, Favorites


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        # rep['image'] = ImageSerializer(instance.product_image.all(), many=True, context=self.context).data
        rep['like'] = LikeSerializer(instance.like.all(), many=True).data
        rep['favorites'] = FavoritesSerializer(instance.favorites.all(), many=True).data

        like = sum([dict(i)['like'] for i in rep['like']])
        rep['like'] = like

        favorites = sum([dict(i)['favorites'] for i in rep['favorites']])
        rep['favorites'] = favorites

        return rep


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProductReview
        fields = ('id', 'author', 'product', 'text', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(author=request.user,  **validated_data)
        return comment


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = ['image', 'id']

    # def get_image_url(self, obj):
    #     if obj.image:
    #         url = obj.image.url
    #         request = self.context.get('request')
    #         if request is not None:
    #             url = request.build_absolute_url(url)
    #     else:
    #         url = ''
    #     return url

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['image'] = self.get_image_url(instance)
    #
    #     return representation


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['author', 'product', 'favorites']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['author', 'product', 'like']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

