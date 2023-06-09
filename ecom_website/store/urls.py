from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('shops', views.all_shops, name = 'all_shops'),
    path('shop/create', views.create_shop, name = 'create_shop'),
    path('shop/update', views.update_shop, name = 'update_shop'),
    path('shop/<int:shop_id>', views.shop, name = 'shop'),
    path('shop/<int:shop_id>/add_product', views.add_product, name = 'add_product'),
    path('shop/<int:product_id>/update_product', views.update_product, name = 'update_product'),
    path('shop/<int:shop_id>/orders', views.shop_orders, name = 'shop_orders'),
    path('shop/<int:shop_id>/products', views.manage_products, name = 'manage_products'),
    path('product/<int:product_id>', views.product, name = 'product'),
    path('products/', views.all_products, name='all_products'),
    path('cart', views.cart, name = 'cart'),
    path('add_to_cart/', views.add_to_cart, name = "add_to_cart"),
    path('checkout/', views.checkout, name = "checkout"),
    path('checkout/<str:session_id>/success', views.checkout_success, name = 'checkout_success'),
    path('orders/', views.my_orders, name = 'my_orders'),
    path('orders/<int:shop_id>/download', views.download_order, name = 'download_orders'),

]
