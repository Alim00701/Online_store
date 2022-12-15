import datetime
from django.shortcuts import render, HttpResponse
from posts.models import Product


def main(request):
    return render(request, 'layouts/index.html')


def posts_view(request):
    if request.method == 'GET':
        posts = Product.objects.all()

        print(posts)

        return render(request, 'posts/posts.html', context={
            'posts': posts
        })


def data(request):
    return HttpResponse(datetime.datetime.now())


def good_by(request):
    return HttpResponse('Good by user!!!')
