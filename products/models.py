from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from datetime import datetime

User = get_user_model()

""" Классы, которые наследуются от models.Model являются моделями, то есть отвечают за связь с БД через ORM.
   В БД будет создана таблица с указанными полями """


class Category(models.Model):
    title = models.CharField(max_length=256)
    # CharField - VARCHAR(), обязательное свойство max_length
    slug = models.SlugField(max_length=256, blank=True, primary_key=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Сategories'


class Product(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=256)
    description = models.TextField()
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    # main_photo = models.ImageField(upload_to='product_photos', blank=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    # image2 = models.ImageField(upload_to='products', blank=True, null=True)
    # image3 = models.ImageField(upload_to='products', blank=True, null=True)
    # image4 = models.ImageField(upload_to='products', blank=True, null=True)

    def __str__(self) -> str:
        return self.title


# class Photo(models.Model):
#     photo = models.ImageField(upload_to='product_photos', blank=True, null=True)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='photos')


class ProductReview(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # photo = models.ImageField(upload_to='photos', blank=True, null=True)


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    """ ForeignKey - поле для свзязи с другой моделью. Обязательное свойство: модель, on_delete - определяет, 
       что произойдет с объявлением, если удалить из БД """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # photo = models.ImageField(upload_to='comment_photos', blank=True, null=True)

    def __str__(self):
        return f'Comment from {self.author.name} to {self.product}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']


class Like(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='like')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='like')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: liked {self.product}'


    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'Likes'


class Favorites(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorites = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: favorites {self.product}'

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'