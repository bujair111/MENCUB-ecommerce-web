from django.urls import path
from . import views
app_name = 'admin1'

urlpatterns=[
    path('mencubadmin', views.mencubadmin, name = 'mencubadmin'),
    path('admin_home', views.admin_home, name = 'admin_home'),
    path('customer_list', views.customer_list, name = 'customer_list'),
    path('seller_list', views.seller_list, name = 'seller_list'),
    path('category', views.category, name = 'category'),
    # path('category_list', views.category_list, name = 'category_list'),
    path('approveseller', views.approveseller, name = 'approveseller'),
    path('admin_login', views.admin_login,name = 'admin_login'),
    path('approve_btn/<int:seller_id>/', views.approve, name = 'approve_btn'),
    path('reject_btn/<int:seller_id>/', views.reject, name = 'reject_btn'),
    path('complaint', views.complaint, name = 'complaint')


]