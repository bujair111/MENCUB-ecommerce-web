from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

from random import sample  # this for set limit for listing

from django.db.models.functions import Random  # this code for show objects in
# random eg'showing all prod in db' /.order_by(random())/

import razorpay
from customer.models import Order, Order_detail
from common.models import Customer
from seller.models import Product, Size, Variants
from mencubadmin.models import Category, Complaints
from .models import CustomerCart
from django.db.models import F  # for annotate
from django.db.models import Q  # for search

from django.core.paginator import Paginator  # not set

# Create your views here.


def master(request):
    get_cust_details = Customer.objects.get(id=request.session['customer'])
    request.session['cust_image'] = get_cust_details
    return render(request, 'cust_templates/master.html', {'c_data': get_cust_details})


def cust_home(request):
    categorys = Category.objects.all()
    c = CustomerCart.objects.filter(
        customer_id=request.session['customer']).count()
    request.session['cart_count'] = c

    get_cust_details = Customer.objects.get(id=request.session['customer'])
    # using to mixedlisting products
    product = Product.objects.order_by(Random())
    # seting limit to how manay carts want to show
    setlimit = sample(list(product), 15)

    context = {
        'c_data': get_cust_details,
        'product': setlimit,
        'cate_list': categorys,
        'c': c
    }
    return render(request, 'cust_templates/cust_home.html', context)


def result(request, cate_id):
    get_cust_details = Customer.objects.get(id=request.session['customer'])
    get_product = Product.objects.filter(category_id=cate_id)

    context = {
        'result': get_product,
        'c':  request.session['cart_count'],
        'c_data': get_cust_details
    }
    return render(request, 'cust_templates/result.html', context)


def cust_profile(request):
    get_cust_details = Customer.objects.get(id=request.session['customer'])
    if request.method == 'POST':
        up_name = request.POST['ed_name']
        up_phone = request.POST['ed_phone']
        up_dob = request.POST['ed_dob']
        up_email = request.POST['ed_email']
        up_gender = request.POST['ed_gender']
        up_address = request.POST['ed_address']

        edit_customer = Customer.objects.filter(id=request.session['customer'])

        if (up_name != ''):
            edit_customer.update(name=up_name)
        else:
            print('else')
        if (up_phone != ''):
            edit_customer.update(phone=up_phone)
        else:
            print('else')
        if (up_dob != ''):
            edit_customer.update(dob=up_dob)
        else:
            print('else')
        if (up_email != ''):
            edit_customer.update(email=up_email)
        else:
            print('else')
        if (up_gender != ''):
            edit_customer.update(gender=up_gender)
        else:
            print('else')
        if (up_address != ''):
            edit_customer.update(address=up_address)
        else:
            print('else')

        try:
            up_image = request.FILES['ed_image']
            get_cust_details.image = up_image
            get_cust_details.save()
        except:
            up_image = None
            
    return render(request, 'cust_templates/cust_profile.html', {'c_data': get_cust_details, 'c':  request.session['cart_count']})


def changepassword(request):
    msg = ''
    if request.method == 'POST':
        oldPass = request.POST['old_pass']
        newPass = request.POST['new_pass']
        try:
            cust_pass = Customer.objects.get(
                id=request.session['customer'], password=oldPass)
            if cust_pass:
                cust_pass.password = newPass
                cust_pass.save()
                msg = 'password change success'
                return redirect('customer:cust_home')
        except:
            msg = 'old pass not match'
    return render(request, 'cust_templates/changepassword.html', {'msg': msg})


def crt_remove(request, product_id, s_id):
    remove_prd = CustomerCart.objects.get(
        product_id=product_id, customer_id=request.session['customer'], size_id=s_id)
    remove_prd.delete()

    return redirect('customer:cart')


def product_details(request, product_id):
    msg = ''

    product_dtl = Product.objects.get(id=product_id)
    available_sizes = Variants.objects.filter(product_id_id=product_id)

    if request.method == 'POST':
        prd_id = Product.objects.get(id=product_id)
        cust_id = Customer.objects.get(id=request.session['customer'])
        size = Variants.objects.get(id=request.POST['size_select'])
        qty = request.POST['qty']
        print(prd_id, cust_id, size)
        check = CustomerCart.objects.filter(product=prd_id, size=size).exists()
        if check:
            msg = 'product existing in cart'
        else:
            new = CustomerCart(
                product=prd_id,
                customer=cust_id,
                size=size,
                qty=qty
            )
            new.save()
            msg = 'added in cart'

    return render(request, 'cust_templates/product_details.html', {'prd_dtl': product_dtl, 'avl_size': available_sizes, 'msg': msg, 'c': request.session['cart_count']})


def cart(request):
    get_cust_details = Customer.objects.get(id=request.session['customer'])
    # ====just profile showing ^======
    cart_data = CustomerCart.objects.filter(customer_id=request.session['customer']).annotate(
        total=F('product__price')*F('qty'))  # annotate us to calculate 2 elements in a row

    grandtotal = 0
    for totals in cart_data:
        grandtotal += totals.total

    tax = (2 * grandtotal)/100
    request.session['tax'] = tax

    totalAmountIncludeTax = grandtotal+tax
    request.session['grand_total_tax'] = totalAmountIncludeTax

    # tax =
    context = {
        'c_data': get_cust_details,
        'data': cart_data,
        'tax': tax,
        'grandtotal': grandtotal,
        'main_total': totalAmountIncludeTax,
        'c':  request.session['cart_count']
    }

    return render(request, 'cust_templates/cart.html', context)


def chechout(request):
    address = Customer.objects.get(id=request.session['customer'])
    cust_address = address.address
    products = CustomerCart.objects.filter(customer_id=request.session['customer']).annotate(
        total=F('product__price')*F('qty'))
    cart_cunt = products.count()
    if cart_cunt <= 0:
        return redirect('customer:cart')
    grandTotal = 0
    for i in products:
        grandTotal += i.total

    tax = request.session['tax']
    total_wite_tax = request.session['grand_total_tax']
    context = {
        'cust_add': cust_address,
        'product': products,
        'total': grandTotal,
        'tax': tax,
        'total_wite_tax': total_wite_tax

    }
    return render(request, 'cust_templates/chechout.html', context)


def help(request):
    if request.method == 'POST':
        text = request.POST['complait']
        customer = request.session['customer']

        new_text = Complaints(
            customer_id=customer,
            complaint=text
        )
        new_text.save()

    return render(request, 'cust_templates/help.html')


def cust_logout(request):

    del request.session['customer']
    request.session.flush()
    return redirect('common:home')


def change_qty_update(request):

    qty = int(request.POST['qty'])
    size = request.POST['size']
    prd_id = request.POST['prd_id']

    stock = Variants.objects.get(product_id_id=prd_id, size_id_id=size)

    if stock.qty > qty:
        max_seting = stock.qty
        change_qty = CustomerCart.objects.get(
            product_id=prd_id, size_id=size, customer_id=request.session['customer'])
        change_qty.qty = qty
        change_qty.save()
        status = True

        qty_change_cart = CustomerCart.objects.annotate(
            total_prc=F('product__price')*F('qty'))
        gr_total = 0

        for i in qty_change_cart:
            gr_total += i.total_prc

        tax = (2 * gr_total)/100
        request.session['tax'] = tax

        totalAmountWitheTax = gr_total+tax
        request.session['grand_total_tax'] = totalAmountWitheTax

        return JsonResponse({'gt_tot': gr_total, 'status': status, 'maxl': max_seting, 'tax': tax, 'main_total': totalAmountWitheTax})
    else:
        status = False
        return JsonResponse({'status': status})


def payment(request):

    if request.method == "POST":
        amount = request.POST['total']
        notes = {'shipping address': 'bomalahalli,bangolre'}

        # RAZOR pay methods
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create(  # creating a new order /(amount and nots sending to razaorpay )
            {"amount": float(amount) * 100, "currency": "INR",
            "payment_capture": "1", 'notes': notes}
        )
        # end

        # creating a oder in oder table (provider id taken by new order creating time / balance detail getting after pyment susses )
        customer = request.session['customer']
        new_oder = Order(
            customer_id=customer,
            amount=request.session['grand_total_tax'],
            provider_order_id=payment['id'],
            status='pending'
        )
        new_oder.save()
        request.session['order_id'] = new_oder.id
        return JsonResponse(payment)


def updatepayment(request):  # this function working after successfully completed payment
    if request.method == "POST":
        amount = request.POST['totalprice']
        paymentId = request.POST['paymentId']
        orderId = request.POST['orderId']
        signId = request.POST['signId']
        orderqty = 0

        # updating order table
        updateOrderDetail = Order.objects.filter(provider_order_id=orderId).update(
            payment_id=paymentId,
            signature_id=signId,
            status='paid'
        )

        # adding oder details into order details table
        order_id = request.session['order_id']
        cartItems = CustomerCart.objects.filter(
            customer=request.session['customer'])

        for singleItem in cartItems:
            new_oder_details = Order_detail(
                customer_id=singleItem.customer_id,
                product_id=singleItem.product_id,
                price=singleItem.product.price,
                quantity=singleItem.qty,
                size=singleItem.size_id,
                payment_status='paid',
                payment_type='razorpay',
                delivery_status='pending',
                order_id=order_id
            )
            new_oder_details.save()

            # stock count reducing (based on customers shopping each products qty)
            orderqty = int(singleItem.qty)
            stockUpdate = Variants.objects.get(
                product_id=singleItem.product_id, size_id=singleItem.size_id)
            stockUpdate.qty = stockUpdate.qty-orderqty
            stockUpdate.save()

        cartItems.delete()

        return JsonResponse({'halo': 'hii'})


def search(request):
    # if case u face any error use this (like local var not found)
    products = Product.objects.none()
    count = 0

    if request.method == 'GET':
        searched = request.GET.get('searched')
        if searched:
            products = Product.objects.filter(
                Q(category__cate_name__icontains=searched) | Q(name__icontains=searched))
            count = products.count()
    context = {
        'result': products,
        'count': count
    }
    return render(request, 'cust_templates/result.html', context)


def oderDetails(request):
    get_cust_details = Customer.objects.get(id=request.session['customer'])
    orderList = Order_detail.objects.filter(
        customer_id=request.session['customer'])
    context = {
        'c_data': get_cust_details,
        'orders_list': orderList
    }

    return render(request, 'cust_templates/oderDetails.html', context)



def allproducts(request):
    get_cust_details = Customer.objects.get(id=request.session['customer'])
    products = Product.objects.all()
    

    context = {
        'count':products.count(),
        'c_data': get_cust_details,
        
        'products': products
    }
    return render(request, 'cust_templates/catelog.html',context)
