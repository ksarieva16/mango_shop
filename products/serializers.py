from rest_framework import serializers
from multiprocessing import context
from products.models import Product, ProductReview, Comment, Category, Like, Favorites
from django.db import IntegrityError
from accounts.models import User


# class PhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photo
#         fields = ['photo']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(author=request.user, **validated_data)
        return comment


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        # rep['image'] = ImageSerializer(instance.product_image.all(), many=True, context=self.context).data
        rep['like'] = LikeSerializer(instance.like.all(), many=True).data
        rep['favorites'] = FavoriteSerializer(instance.favorites.all(), many=True).data

        like = sum([dict(i)['like'] for i in rep['like']])
        rep['like'] = like

        favorites = sum([dict(i)['favorites'] for i in rep['favorites']])
        rep['favorites'] = favorites

        return rep


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = ProductReview
        fields = ('id', 'author', 'product', 'text', 'created_at')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['author'] = user

        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['author', 'product', 'like']
