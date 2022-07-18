from django.contrib import admin

from products.models import Category, Product, Comment, Favorites, Like, Image


class ProductImageInLine(admin.TabularInline):
    model = Image
    max_num = 10
    min_num = 1

#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     # model = Product
#     inlines = [ProductImageInLine, ]


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Favorites)
