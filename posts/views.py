import datetime
from django.shortcuts import render, HttpResponse, redirect
from posts.forms import ProductCreateForm, CommentCreateForm
from posts.models import Product, Category, Review


PAGINATION_LIMIT = 6


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
            'categories': categories,
            'user': None if request.user.is_anonymous else request.user
        }

        return render(request, 'categories/index.html', context=context)


def posts_view(request):
    if request.method == 'GET':
        category_id = int(request.GET.get('category_id', 0))
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if category_id:
            products = Product.objects.filter(categories__in=[category_id])
        else:
            products = Product.objects.all()

        max_page = products.__len__() / PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1

        max_page = int(max_page)
        products = products[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]

        if search:
            products = products.filter(title__iscontains=search)

        return render(request, 'posts/posts.html', context={
            'products': products,
            'user': None if request.user.is_anonymous else request.user,
            'max_page': range(1, max_page+1)
        })


def product_detail_view(request, id):
    if request.method == 'GET':
        posts = Product.objects.get(id=id)

        context = {
            'posts': posts,
            'reviews': posts.reviews.all(),
            'categories': posts.caregories.all(),
            'comment_form': CommentCreateForm,
            'user': None if request.user.is_anonymous else request.user
        }

        return render(request, 'posts/review.html', context=context)

    if request.method == 'POST':
        post = Product.objects.get(id=id)
        form = CommentCreateForm(date=request.POST)

        if form.is_valid():
            Review.objects.create(
                author=request.user,
                post_id=id,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/posts/{id}/')
        else:
            return render(request, 'posts/review.html', context={
                'post': post,
                'reviews': post.reviews.all(),
                'categories': post.caregories.all(),
                'comment_form': form,
                'user': None if request.user.is_anonymous else request.user
            })


def product_create_view(request):
    if request.method == 'GET':
        return render(request, 'posts/create.html', context={
            'form': ProductCreateForm
        })

    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)

        if form.is_valid():
            Product.objects.create(
                auth=request.user,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate', 0)
            )

            return redirect('/posts/')
        else:
            return render(request, 'posts/create.html', context={
                'form': form,
                'user': None if request.user.is_anonymous else request.user
            })
