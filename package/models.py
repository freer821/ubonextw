from django.db import models

# Create your models here.
class Package(models.Model):
    package_no = models.CharField(max_length=30, unique=True, blank=True,null=True)
    sender = models.CharField(max_length=50, default="")
    sender_addr = models.CharField(max_length=225, default="")
    sender_tel = models.CharField(max_length=50,default="")
    receiver = models.CharField(max_length=50, default="")
    receiver_addr = models.CharField(max_length=225, default="")
    receiver_tel = models.CharField(max_length=50,default="")
    inland_code = models.CharField(max_length=30, unique=True, blank=True,null=True)
    goods_descr= models.TextField(default="")
    goods_quantity= models.CharField(max_length=50, default="")
    des_code = models.CharField(max_length=30, default="")
    sf_monthcard_no = models.CharField(max_length=30, default="")
    logistic_product = models.CharField(max_length=30, default="")
    comment = models.TextField(default="")