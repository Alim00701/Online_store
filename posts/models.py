from django.db import models


class Category(models.Model):
    title = models.CharField('Категория', max_length=50)


class Product(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_date = models.DateField(auto_now=True)
    modified_date = models.DateField(auto_now_add=True)
    comments = models.CharField(max_length=235)
    categories = models.ManyToManyField(Category)


class Review(models.Model):
    posts = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews')
    text = models.TextField()
    created_date = models.DateField(auto_now=True)
