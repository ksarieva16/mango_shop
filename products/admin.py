from django.contrib import admin

from products.models import Category, Product, Comment, Favorites, Like




#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     # model = Product
#     inlines = [ProductImageInLine, ]


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
# admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Favorites)
