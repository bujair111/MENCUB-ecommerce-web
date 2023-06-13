from django.shortcuts import render, redirect
from common.models import Admin1, Seller, Customer
from seller.models import Product
from .models import Category, Complaints
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from customer.models import Order_detail
import random

# Create your views here.


def admin_login(request):

    msg = ''
    if request.method == 'POST':
        enterdemail = request.POST['email']
        enterdpass = request.POST['password']

        try:
            getadmin = Admin1.objects.get(
                email=enterdemail, admin_pass=enterdpass)
            request.session['admin'] = getadmin.id
            return redirect('admin1:admin_home')
        except:
            msg = 'mail or pass error'

    return render(request, 'admin_temp/adminlogin.html', {'msg': msg})


def mencubadmin(request):
    return render(request, 'admin_temp/admin_master.html')


def admin_home(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    sellers = Seller.objects.all()
    complaints = Complaints.objects.all()
    orders = Order_detail.objects.order_by('date')[:6]


    context = {
        'customer_list': customers,
        'customer_count': customers.count(),
        'product_count': products.count(),
        'sellers_count': sellers.count(),
        'complaints_count': complaints.count(),
        'order_details': orders

    }
    return render(request, 'admin_temp/admin_home.html', context)

# ====customer list=====


def customer_list(request):

    total_coustomers = Customer.objects.all()
    return render(request, 'admin_temp/customer_list.html', {'cust': total_coustomers})

# ======seller list======


def seller_list(request):

    total_sellers = Seller.objects.filter(status='approved')
    return render(request, 'admin_temp/seller_list.html', {'list': total_sellers})


def category(request):

    categories = Category.objects.all()
    msg = ''
    if request.method == 'POST':
        c_name = request.POST['cate_name']
        c_dic = request.POST['cate_des']
        print(c_name, c_dic)
        try:
            c_image = request.FILES['cate_image']
        except:
            c_image = None

        new_cate = Category(
            cate_name=c_name,
            cate_description=c_dic,
            cate_image=c_image
        )
        new_cate.save()
        msg = 'category added'
    return render(request, 'admin_temp/category.html', {'cat': categories, 'msg': msg})


# ======request list========
def approveseller(request):

    sellers = Seller.objects.filter(status='pending')
    return render(request, 'admin_temp/approveseller.html', {'data': sellers})


# ====approveing =======
def approve(request, seller_id):

    seller = Seller.objects.get(id=seller_id)
    seller.status = 'approved'

    name = seller.name
    semail = seller.s_email

    intno = random.randint(111, 999)
    password1 = 'seller' + name.lower() + str(intno)
    seller.password = password1
    massage = 'hi ' + name + ' your MENCUB account password is ' + password1

    send_mail(
        'you ar approved as a men cub seller ',
        massage,
        settings.EMAIL_HOST_USER,
        [semail],
        fail_silently=False
    )
    seller.save()

    return redirect('admin1:approveseller')
# ============================


def reject(request, seller_id):

    seller = Seller.objects.get(id=seller_id)
    name = seller.name
    email = seller.s_email
    massage = 'hi ' + name + \
        'sorry for the inconvenience you are no eligible for our terms and conditions MENCUB.india '
    print('rejected')
    send_mail(
        'Rejected',
        massage,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
    seller.delete()
    return redirect('admin1:approveseller')


def complaint(request):
    complaints = Complaints.objects.all()
    return render(request, 'admin_temp/complaint.html', {'complaints': complaints})
