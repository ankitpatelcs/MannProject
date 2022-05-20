
from . import views
from django.urls import path

urlpatterns = [   
    path('',views.seller_login,name='seller-login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add-product/',views.add_product,name='add-product'),
    path('manage-products/',views.manage_products,name='manage-products'),
    path('delete-product/<int:pid>',views.delete_product,name='delete-product'),
    path('edit-product/<int:pid>',views.edit_product,name='edit-product'),
   
]