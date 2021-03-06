from rest_framework import serializers
from products.models import Product, Comment, Category, Like, Favorites, Rating
from .utils import get_rating
from django.contrib.auth import get_user_model

User = get_user_model()


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
        rep['rating'] = get_rating(rep.get('id'), Product)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        # rep['image'] = ImageSerializer(instance.product_image.all(), many=True, context=self.context).data
        rep['like'] = LikeSerializer(instance.like.all(), many=True).data
        rep['favorites'] = FavoriteSerializer(instance.favorites.all(), many=True).data

        like = sum([dict(i)['like'] for i in rep['like']])
        rep['like'] = like

        favorites = sum([dict(i)['favorites'] for i in rep['favorites']])
        rep['favorites'] = favorites
        rep['username'] = User.objects.get(email=rep['user']).name
        rep['author'] = str(self.context.get('request').user) == str(rep['user'])

        return rep

    def save(self, **kwargs):
        email = self.context.get('request').user
        self.validated_data['user'] = email
        return super().save(**kwargs)

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance

#
# class ReviewSerializer(serializers.ModelSerializer):
#     author = serializers.ReadOnlyField(source='author.email')
#
#     class Meta:
#         model = ProductReview
#         fields = '__all__'
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         validated_data['author'] = user
#
#         return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['author', 'product', 'favorites']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['author', 'product', 'like']


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product = validated_data.get('product')

        if Rating.objects.filter(author=user, product=product):
            rating = Rating.objects.get(author=user, product=product)
            return rating

        rating = Rating.objects.create(author=request.user, **validated_data)
        return rating