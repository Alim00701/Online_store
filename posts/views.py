import datetime
from django.shortcuts import render, HttpResponse, redirect
from posts.forms import ProductCreateForm, CommentCreateForm
from posts.models import Product, Category, Review
from django.views.generic import ListView, CreateView


PAGINATION_LIMIT = 6


class PostsCBV(ListView):
    queryset = Product.objects.all()
    template_name = 'posts/posts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'posts': kwargs['posts'],
            'max_page': kwargs['max_page'],
            'user': kwargs['user']
        }
    
    def get(self, request, **kwargs):
        category_id = int(request.GET.get('category_id', 0))
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if category_id:
            products = Product.objects.filter(categories__in=[category_id])
        else:
            products = Product.objects.all()

        if search:
            products = products.filter(title__iscontains=search)

        max_page = products.__len__() / PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1

        max_page = int(max_page)
        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        return render(request, self.template_name, context=self.get_context_data(
            products=products,
            user=None if request.user.is_anonymous else request.user,
            max_page=range(1, max_page + 1)
        ))


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


def main(request):
    return HttpResponse('Hello! Its my project')


def data(request):
    return HttpResponse(datetime.datetime.now())


def good_by(request):
    return HttpResponse('Good by user!!!')


def main_view(request):
    return render(request, 'layouts/index.html')


class CategoriesCBV(ListView):
    model = Category
    template_name = 'categories/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'categories': self.get_queryset(),
            'user': self.request.user if not self.request.user.is_anonymous else None
        }


def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()

        context = {
            'categories': categories,
            'user': None if request.user.is_anonymous else request.user
        }

        return render(request, 'categories/index.html', context=context)


class ProductDetailCBV(ListView):
    template_name = 'posts/review.html'
    form_class = CommentCreateForm
    model = Product
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'product': kwargs['product'],
            'reviews': kwargs['reviews'],
            'categories': kwargs['categories'],
            'review_form': kwargs['review_form']

        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                auther_id=request.user.id,
                text=form.cleaned_data.get('text'),
                product_id=kwargs['id'],
            )
            return redirect(f'/products/{kwargs["id"]}/')

        else:
            return render(request, self.template_name, context=self.get_context_data(
                form=form,
                product=Product.objects.get(id=kwargs['id'])
            ))

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs["id"])
        reviews = Review.objects.filter(product_id=kwargs["id"])
        categories = product.categories.all()

        return render(request, self.template_name, context=self.get_context_data(
            reviews=reviews,
            categories=categories,
            product=Product.objects.get(id=kwargs['id']),
            review_form=CommentCreateForm
        ))


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


class ProductsCreateCBV(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'posts/create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'user': self.request.user if not self.request.user.is_anonymous else None,
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            self.model.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
                rating=form.cleaned_data.get('rating')
            )
            return redirect('/products')
        else:
            return render(request, self.template_name, context=self.get_context_data(form=form))


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
