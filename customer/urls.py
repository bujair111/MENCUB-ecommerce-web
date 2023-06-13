from django.urls import path
from . import views

app_name = 'customer'



urlpatterns=[
    path('master', views.master, name='master'),
    path('cust_home', views.cust_home, name='cust_home'),
    path('cust_profile', views.cust_profile, name='cust_profile'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('cart', views.cart, name='cart'),
    path('product_details/<int:product_id>', views.product_details, name='product_details'),
    path('chechout', views.chechout, name='chechout'),
    path('help', views.help, name='help'),
    path('cust_logout', views.cust_logout, name='cust_logout'),
    path('crt_remove/<int:product_id>/<int:s_id>/', views.crt_remove, name='crt_remove'),
    path('result/<int:cate_id>',  views.result, name ='result'),
    path('change_qty_update',  views.change_qty_update, name ='change_qty_update'),
    path('search/', views.search, name='search'),
    path('payment', views.payment, name='payment'),
    path('updatepayment', views.updatepayment, name='updatepayment'),
    path('oderDetails', views.oderDetails, name='oderdeDails'),
    path('allproducts', views.allproducts, name='allproducts')




]