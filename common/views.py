from random import sample
from django.conf import settings
from django.shortcuts import render,redirect
from django.db.models.functions import Random

from common.models import Customer,Seller
from mencubadmin.models import Category
from django.http import JsonResponse
from django.core.mail import send_mail
from seller.models import Product,Variants
from django.db.models import Q  # for search


# Create your views here.
def home(request):
    product = Product.objects.order_by(Random())
    setLimit = sample(list(product),12)
    all_catgory = Category.objects.all()

    context ={
        'catelist': all_catgory,
        'productList': setLimit
        
    }
    return render(request, 'common_temp/home.html', context)


# ===customer login===
def cust_login(request):
    msg=''
    if request.method == 'POST':
        user_password = request.POST['password']
        user_email = request.POST['email']
        try:
            get_customer = Customer.objects.get(email = user_email, password = user_password)
            request.session['customer']=get_customer.id
            print(get_customer.id)
            return redirect('customer:cust_home')
        except:
            msg ='invalid mail or password'    
    
    return render(request, 'common_temp/cust_login.html', {'msg': msg})
# === ===

# ===customer signup
def cust_signup(request):
    msg=''
    if request.method == 'POST':
        cname = request.POST['name']
        cemail = request.POST['email']
        cphone = request.POST['phone']
        cgender = request.POST['gender']
        cdob = request.POST['dob']
        caddress = request.POST['address']
        cpassword = request.POST['password']
        crepassword = request.POST['rePassword']
        try:
            cimage = request.FILES['custImage']
        except:
            cimage = None
        

        if cpassword == crepassword:
            new_customer = Customer(
                name = cname,
                phone = cphone,
                dob = cdob,
                email = cemail,
                gender = cgender,
                address = caddress,
                image = cimage,
                password = cpassword
            )
            msg='account created'
            new_customer.save()
        else:
            msg = 'enter same password'

    return render(request, 'common_temp/cust_signup.html', {'msg': msg})
# ===== ====

# ======seller signup==========
def seller_signup(request):

    msg =''
    if request.method == 'POST':
        sname = request.POST['name']
        semail = request.POST['email']
        sgender = request.POST['gender']
        sdob = request.POST['dob']
        sphone = request.POST['phone']
        saddress = request.POST['address']
        scompanyname = request.POST['company_name']
        accno = request.POST['acc_number']
        ifsc = request.POST['ifsc']
        accholder = request.POST['acc_holder']
        image = request.FILES['image']
        

        newseller = Seller(
            name = sname,
            s_email = semail,
            gender = sgender,
            dob = sdob,
            phone = sphone,
            address = saddress,
            companyName = scompanyname,
            accNo = accno,
            ifsc = ifsc,
            accHolder = accholder,
            image = image
        )
        newseller.save()
        msg = '"your request submitted our admin send your password after validating details on your registered mail"'
    
    return render(request, 'common_temp/seller_signup.html', {'msg': msg})

# email exists check on input time
def seller_mail_exist(request):

    mail = request.POST['email']
    status = Seller.objects.filter(s_email= mail).exists()
    return JsonResponse({'status': status})

# =======end=========

def seller_login(request):

    msg=''
    if request.method == 'POST':
        seller_password = request.POST['pass']
        seller_email = request.POST['email']
        try:
            get_seller = Seller.objects.get(s_email = seller_email,password = seller_password)
            request.session['seller']=get_seller.id
            print(get_seller.id)
            return redirect('seller:seller_home')
        except:
            msg ='invalid mail or password'    
    return render(request, 'common_temp/seller_login.html', {'msg': msg})

def mail_exist(request):
    print('goootit ')
    mail = request.POST['email']
    status = Customer.objects.filter(email= mail).exists()
    return JsonResponse({'status': status})


def cust_forget(request):

    msg =''
    if request.method=='POST':
        entered_email = request.POST['forget_mail']
        try:
            check=Customer.objects.get(email = entered_email)
            password=check.password
            send_mail(
                'your password is',
                password,
                settings.EMAIL_HOST_USER,
                [entered_email],
                fail_silently = False
            )
            msg='your password is sand to your mail check it now'
        except:
            msg = 'enter registered email'
    return render(request, 'common_temp/forgetpass.html', {'msg': msg})

def result(request):
    all_catgory = Category.objects.all()

    return render(request, 'common_temp/result.html', {'catelist': all_catgory,} )


def search(request):

    products = Product.objects.none()
    count = 0

    if request.method == 'GET':
        search = request.GET.get('searched_data')
        if search:
            products = Product.objects.filter(
                Q(category__cate_name__icontains=search) | Q(name__icontains=search))
            count= products.count()
    context = {
        'result': products,
        'count': count
    }
    return render(request, 'common_temp/result.html', context)
    

def filter(request, cate_id):
    print(cate_id)
    count = 0
    filter_data = Product.objects.filter(category= cate_id)
    context={
        'result': filter_data,
        'count': filter_data.count()
    }
    return render(request, 'common_temp/result.html', context)
        



def viewproduct(request,p_id):
    all_catgory = Category.objects.all()

    product_dtl = Product.objects.get(id=p_id)
    available_sizes = Variants.objects.filter(product_id_id=p_id)
    
    return render(request, 'common_temp/viewproduct.html', {'prd_dtl': product_dtl, 'avl_size': available_sizes,'catelist':all_catgory})



