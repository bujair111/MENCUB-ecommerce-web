from django.shortcuts import render,redirect
from common.models import Seller
from seller.models import Product,Size,Variants
from mencubadmin.models import Category
from django.http import JsonResponse
from django.core import serializers
from customer.models import *
from django.db.models import F  # for annotate

from twilio.rest import Client
from django.conf import settings
from phonenumbers import parse, PhoneNumberFormat




# Create your views here.
def seller_master(request):

    seller = Seller.objects.get(id = request.session['seller'])
    return render(request, 'seller_temp/seller_master.html', {'data': seller})

def seller_home(request):

    seller = Seller.objects.get(id = request.session['seller'])
    product = Product.objects.filter(seller_id = request.session['seller']).values('cover_image','name','price','prd_no')
    
    context = {
        'data':seller,
        'prd':product
    }
    return render(request, 'seller_temp/seller_home.html', context)



def add_product(request):

    seller = Seller.objects.get(id = request.session['seller'])
    category_list = Category.objects.all()
    msg = ''
    if request.method == 'POST':
        p_name = request.POST['name']
        p_no = request.POST['prd_no']
        p_category = request.POST['category']
        p_details = request.POST['details']
        p_price = request.POST['price']
        seller_id = request.session['seller']
        try:
            p_cover = request.FILES['cover_image']
            p_image1 = request.FILES['image2']
            p_image2 = request.FILES['image3']
        except:
            p_cover = None
            p_image1 = None   
            p_image2 = None 
        
        new_prd = Product(
            name = p_name,
            prd_no = p_no,
            category_id = p_category,
            details = p_details,
            price = p_price,
            cover_image = p_cover,
            image1 = p_image1,
            image2 = p_image2, 
            seller_id = seller_id
        )
        msg = 'product added'
        new_prd.save()
    context = {
        'data':seller,
        'catelist':category_list,
        'msg':msg
    }    
    return render(request, 'seller_temp/add_product.html', context)


def view_orders(request):
    orders = Order_detail.objects.filter(product__seller_id = request.session['seller']).annotate(
        total =F('price')*F('quantity'))
    
    
    context ={
        'oder_list': orders
    }
    return render(request, 'seller_temp/view_orders.html', context)


def update_stock(request):
    seller = Seller.objects.get(id = request.session['seller'])
    totale_cate = Category.objects.all()
    
    total = Size.objects.all()
    
    context = {
        'data':seller,
        'cate':totale_cate,
        'size':total
    }
    return render(request, 'seller_temp/update_stock.html', context)


def seller_profile(request):
    seller = Seller.objects.get(id = request.session['seller'])
    return render(request, 'seller_temp/seller_profile.html', {'data': seller})


def password(request):
    msg = ''
    if request.method  == 'POST':
        oldpass = request.POST['oldpass']
        newpass = request.POST['newpass']
        try:
            get_seller = Seller.objects.get(id = request.session['seller'],password = oldpass)
            if get_seller:
                get_seller.password = newpass
                get_seller.save()
                msg = 'password changed'
                return redirect('seller:seller_home')
        except:
            msg = 'old pss not match'
    return render(request, 'seller_temp/password.html', {'msg': msg})




# ==================selected prd details================
def view_prd(request):
    cateid = request.POST['cateid']
    c_prd = Product.objects.filter(category = cateid,seller = request.session['seller'])

    # ===== if u want to avoid using of serializers. use the method make a dict for you need data's 
    # = hir we doing setting obj in a (for in loop)
    data =[{'id':c_prd1.id,'prd_no':c_prd1.prd_no} for c_prd1 in c_prd]

    return JsonResponse({'data':data})





def selected_prd_img_name(request):
    product_id = request.POST['select_prd_id']
    get_product = Product.objects.get(id = product_id)
    data ={'name':get_product.name}

    curent_stock = Variants.objects.filter(product_id_id=product_id)
    converted_data = [{'size':curent_stock1.size_id.sizes,'qty':curent_stock1.qty}for curent_stock1 in curent_stock ]
    print(converted_data)
    return JsonResponse({'data':data,'stock':converted_data})

# =============================================



# hire updating prd difrent sizes stock if any prd size already in a column we update the stock
def add_variants(request):
    msg = ''
    product = request.POST['product_id']
    size = request.POST['selected_size']
    new_qty = request.POST['qty']
    product = Product.objects.get(id=product)
    size = Size.objects.get(id=size)

    check = Variants.objects.filter(size_id_id=size, product_id_id=product).exists()
    if check:
        check1 = Variants.objects.get(size_id_id=size, product_id_id=product)
        balance_qty = check1.qty
        total = balance_qty + int(new_qty)
        updating = Variants.objects.filter(size_id_id=size, product_id_id=product).update(qty=total)
        print('halppppp', total)
        
    else:
        new_ver = Variants(
            product_id=product,
            size_id=size,
            qty=new_qty
        )
        new_ver.save()
    msg = 'product stock updated'
    return JsonResponse({'msg': msg})




def seller_signout(request):
    del request.session['seller']
    request.session.flush()
    return redirect('common:home')


def check_out(request,order_id):
    
    delivered_order = Order_detail.objects.get(id = order_id)
    Product_name = delivered_order.product.name

    customer_phone =  str(delivered_order.customer.phone)
    
    delivered_order.delivery_status = 'delivered'
    delivered_order.save()
    

    phone_number = parse(customer_phone, "IN")
    number = "+{}".format(phone_number.country_code) + "{}".format(phone_number.national_number)

    # Twilio api setting 

    message_body = "tanks for shopping MENCUB your  "+Product_name+"is shipped"  # Replace with the message you want to send
    to_number = number  # Get the phone number from the query string
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=message_body,
        to=to_number,
        from_=settings.TWILIO_PHONE_NUMBER
    )
    return redirect ('seller:view_orders')