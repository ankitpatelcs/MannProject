
from . import views
from django.urls import path
from django.contrib import admin


urlpatterns = [   
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('products/',views.products,name='products'),
    path('single/<int:pid>',views.single,name='single'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('pay/', views.pay, name='pay'),
    path('otp/', views.otp, name='otp'),
]