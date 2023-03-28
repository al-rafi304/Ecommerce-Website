from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_member, name ='login'),
    path('logout', views.logout_member, name ='logout'),
]
