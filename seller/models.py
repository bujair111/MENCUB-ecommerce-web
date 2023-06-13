from django.db import models
from mencubadmin.models import Category
from common.models import Seller


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=30)
    prd_no = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    details = models.CharField(max_length=200)
    price = models.IntegerField()
    cover_image = models.ImageField(upload_to='product/')
    image1 = models.ImageField(upload_to='product/')
    image2 = models.ImageField(upload_to='product/')
    seller = models.ForeignKey(Seller, default='', on_delete = models.CASCADE)

    class Meta:
        db_table = 'product'

class Size(models.Model):
    sizes = (models.CharField(max_length=5))

    class Meta:
        db_table = 'size'    

class Variants(models.Model):
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE)
    size_id = models.ForeignKey(Size, on_delete = models.CASCADE)
    qty = models.IntegerField()

    class Meta:
        db_table = 'variants'