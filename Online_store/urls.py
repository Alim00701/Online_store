"""Online_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from posts.views import main, data, good_by, posts_view, product_detail_view, categories_view, product_create_view, \
    PostsCBV, ProductDetailCBV, ProductsCreateCBV, CategoriesCBV
from django.conf.urls.static import static
from Online_store import settings
from users.views import login_view, logout_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('posts/', PostsCBV.as_view()),
    path('data/', data),
    path('goodby/', good_by),
    path('posts/<int:id>/', ProductDetailCBV.as_view()),
    path('product/create/', ProductsCreateCBV.as_view()),
    path('categories/', CategoriesCBV.as_view()),
    path('users/login/', login_view),
    path('users/logout/', logout_view),
    path('users/register/', register_view)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
