from django.urls import path
from . import views

app_name = 'common'

urlpatterns=[
    path('mencub', views.home, name='home'),
    path('cust_login', views.cust_login, name='cust_login'),
    path('cust_signup', views.cust_signup, name='cust_signup'),
    path('seller_signup', views.seller_signup, name='seller_signup'),
    path('seller_login', views.seller_login, name='seller_login'),
    path('mail_exist', views.mail_exist, name='mail_exist'),
    path('cust_forget', views.cust_forget, name='cust_forget'),
    path('seller_mail_exist', views.seller_mail_exist, name='seller_mail_exist'),
    path('result',views.result, name='result'),
    path('search', views.search, name='search'),
    path('filter/<int:cate_id>', views.filter, name='filter'),
    path('viewproduct/<int:p_id>', views.viewproduct, name='viewproduct')

]