from django.urls import path
from . import views

app_name = 'seller'


urlpatterns = [
    path('seller_master', views.seller_master, name = 'seller_master'),
    path('seller_home', views.seller_home, name = 'seller_home'),
    path('add_product', views.add_product, name = 'add_product'),
    path('view_orders', views.view_orders, name = 'view_orders'),
    path('update_stock', views.update_stock, name = 'update_stock'),
    path('seller_profile', views.seller_profile, name = 'seller_profile'),
    path('password', views.password, name = 'password'),
    path('view_prd', views.view_prd, name = 'view_prd'),
    path('selected_prd_img_name',  views.selected_prd_img_name, name ='selected_prd_img_name'),
    path('add_variants',  views.add_variants, name ='add_variants'),
    path('seller_signout',  views.seller_signout, name ='seller_signout'),
    path('check_out/<int:order_id>',  views.check_out, name ='check_out')
    
]
