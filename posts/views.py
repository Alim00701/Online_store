import datetime
from django.shortcuts import render, HttpResponse
from posts.models import Product, Category, Review


def main(request):
    return HttpResponse('Hello! Its my project')


def data(request):
    return HttpResponse(datetime.datetime.now())


def good_by(request):
    return HttpResponse('Good by user!!!')


def main_view(request):
    return render(request, 'layouts/index.html')


def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()

        context = {
            'categories': categories
        }

        return render(request, 'categories/index.html', context=context)


def posts_view(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id', 0)

        if category_id:
            products = Product.objects.filter(categories__in=[category_id])
        else:
            products = Product.objects.all()

        return render(request, 'posts/posts.html', context={
            'products': products
        })


def product_detail_view(request, id):
    if request.method == 'GET':
        post = Product.objects.get(id=id)

        context = {
            'post': post,
            'reviews': Review.objects.filter(posts=post),
            'categories': post.caregories.all()
        }

        return render(request, 'posts/review.html', context=context)
