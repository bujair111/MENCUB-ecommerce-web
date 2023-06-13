from datetime import date
from django.db import models
from seller.models import Product,Variants
from common.models import Customer
from seller.models import Product

# Create your models here.
class CustomerCart(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    size = models.ForeignKey(Variants, on_delete= models.CASCADE)
    qty = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart'

class Order(models.Model):
    customer =models.ForeignKey(Customer,on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=20,default="pending")
    provider_order_id = models.CharField(max_length=40)
    payment_id = models.CharField(max_length=36)
    signature_id = models.CharField(max_length=128)

    class Meta:
        db_table = 'order_table'


class Order_detail(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    size = models.CharField(max_length=20,default='')
    date = models.DateField(default=date.today)
    payment_status = models.CharField(max_length=20,default="pending") #update after payment confirmed
    payment_type = models.CharField(max_length=20)
    delivery_status = models.CharField(max_length=30)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)



    class Meta:
        db_table = 'order_detail'