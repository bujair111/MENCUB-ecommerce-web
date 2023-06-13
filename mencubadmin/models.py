from django.db import models
from common.models import Customer

# Create your models here.

class Category(models.Model):
    cate_name = models.CharField(max_length=30)
    cate_description = models.CharField(max_length=500)
    cate_image = models.ImageField(upload_to='category/')

    class Meta:
        db_table = 'category'

class Complaints(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    complaint = models.CharField(max_length=500)

    class Meta :
        db_table = 'complaints'         