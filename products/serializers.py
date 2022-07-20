from rest_framework import serializers
from multiprocessing import context
from products.models import Product, ProductReview, Comment, Category, Like, Favorites
from django.db.utils import IntegrityError


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

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
    #     # rep['image'] = ImageSerializer(instance.product_image.all(), many=True, context=self.context).data
    #     rep['like'] = LikeSerializer(instance.like.all(), many=True).data
    #     rep['favorites'] = FavoriteSerializer(instance.favorites.all(), many=True).data
    #
    #     like = sum([dict(i)['like'] for i in rep['like']])
    #     rep['like'] = like
    #
    #     favorites = sum([dict(i)['favorites'] for i in rep['favorites']])
    #     rep['favorites'] = favorites
    #
    #     return rep


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = ProductReview
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['author'] = user

        return super().create(validated_data)



class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Favorites
        fields = '__all__'

    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user
        return super().validate(attrs)

    def create(self, validated_data):
        user = validated_data['user']
        product = validated_data['product']
        if Favorites.objects.filter(user=user, product=product):
            Favorites.objects.filter(user=user, product=product).delete()
            validated_data = {}
            return super().create(validated_data)
        else:
            return super().create(validated_data)

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except IntegrityError:
            print('')


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user
        return super().validate(attrs)

    def create(self, validated_data):
        user = validated_data['user']
        product = validated_data['product']
        if Like.objects.filter(user=user, product=product):
            Like.objects.filter(user=user, product=product).delete()
            validated_data = {}
            return super().create(validated_data)
        else:
            return super().create(validated_data)

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except IntegrityError:
            print('')
