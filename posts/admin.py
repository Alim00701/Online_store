from django.contrib import admin
from posts.models import Product, Review, Category


admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Category)
