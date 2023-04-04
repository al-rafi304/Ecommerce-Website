from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('shop/create', views.create_shop, name = 'create_shop'),
    path('shop/<int:shop_id>', views.shop, name = 'shop'),
    path('shop/<int:shop_id>/add_product', views.add_product, name = 'add_product'),
    path('shop/<int:shop_id>/orders', views.shop_orders, name = 'shop_orders'),
    path('product/<int:product_id>', views.product, name = 'product'),
    path('cart', views.cart, name = 'cart'),
    path('add_to_cart/', views.add_to_cart, name = "add_to_cart"),
    path('checkout/', views.checkout, name = "checkout"),
    path('checkout/<str:session_id>/success', views.checkout_success, name = 'checkout_success'),
    path('orders/', views.my_orders, name = 'my_orders'),

    path('test', views.test, name = 'test'),
]
