from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField('Категория', max_length=50)


class Product(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_date = models.DateField(auto_now=True)
    modified_date = models.DateField(auto_now_add=True)
    comments = models.CharField(max_length=235)
    categories = models.ManyToManyField(Category)


class Review(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    posts = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews')
    text = models.TextField()
    created_date = models.DateField(auto_now=True)
