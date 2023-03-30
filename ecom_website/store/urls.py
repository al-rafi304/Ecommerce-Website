from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('shop/create', views.create_shop, name = 'create_shop'),
    path('shop/<int:shop_id>', views.shop, name = 'shop'),
    path('shop/<int:shop_id>/add_product', views.add_product, name = 'add_product'),
    path('product/<int:product_id>', views.product, name = 'product'),
]
