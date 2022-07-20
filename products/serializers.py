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
        comment = Comment.objects.create(author=request.user,  **validated_data)
        return comment


class ProductSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(read_only=True)
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


    #     action = self.context.get('action')
    #     if action == 'retrieve':
    #         photos = PhotoSerializer(instance.photos.all(), many=True).data
    #         photos.append({"photo": "media/" + ''.join(representation['main_photo'].split('media')[1:])})
    #         representation['photos'] = photos
    #         comments = CommentSerializer(instance.comments.all(), many=True).data
    #         representation['comments'] = comments
    #         representation.pop('main_photo')
    #     elif action == 'list':
    #         comments = CommentSerializer(instance.comments.all(), many=True).data
    #         if not comments:
    #             representation['comments'] = []
    #         else:
    #             representation['comments'] = comments[0]
    #     return representation
    #
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     images_data = request.FILES
    #     product = Product.objects.create(author=request.user, **validated_data)
    #
    #     for photo in images_data.getlist('photos'):
    #         Photo.objects.create(photo=photo, product=product)
    #     return product
    #
    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     images_data = request.FILES
    #     instance.images.all().delete()
    #     for photo in images_data.getlist('photos'):
    #         Photo.objects.create(photo=photo, product=instance)
    #     return instance


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

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     favourite = Favorites.objects.create(user=user, **validated_data)
    #     return favourite
    #
    # def to_representation(self, instance):
    #     representation = super(FavoriteSerializer, self).to_representation(instance)
    #     representation['user'] = instance.user.email
    #     return representation


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['author', 'product', 'like']


