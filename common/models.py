from django.db import models
from datetime import date

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=30)
    phone = models.BigIntegerField()
    dob = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    gender = models.CharField(max_length=15)
    address = models.CharField(max_length=500)
    image = models.ImageField(upload_to='customer/')
    password = models.CharField(max_length=100)
    joinDate = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'customer'


class Seller(models.Model):
    name = models.CharField(max_length=20)
    s_email = models.CharField(max_length=100,default='')
    gender = models.CharField(max_length=20)
    dob = models.CharField(max_length=20)
    phone = models.BigIntegerField()
    address = models.CharField(max_length=300)
    companyName = models.CharField(max_length=50)
    accNo = models.BigIntegerField()
    ifsc = models.CharField(max_length=50)
    accHolder = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    image = models.ImageField(upload_to='seller/')
    status = models.CharField(max_length=20,default="pending")
    joinData = models.DateField(default=date.today)

    class Meta:
        db_table = 'seller'

class Admin1(models.Model):
    email = models.CharField(max_length=30)
    admin_pass = models.CharField(max_length=30)

    class Meta:
        db_table = 'admintb'