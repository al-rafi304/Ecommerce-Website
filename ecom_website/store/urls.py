from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('store/create', views.create_shop, name = 'create_shop'),
]
