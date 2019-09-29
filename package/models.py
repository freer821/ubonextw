from django.db import models


def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise Exception(('%(value)s is not an integer or a float  number'), params={'value': value})

# Create your models here.
class Package(models.Model):
    logistic_product = models.CharField(max_length=30, default="")
    package_no = models.CharField(max_length=30, unique=True, blank=True,null=True)
    receiver_identity = models.CharField(max_length=20,default="")
    receiver_name = models.CharField(max_length=50, default="")
    receiver_tel = models.CharField(max_length=20,default="")
    receiver_email = models.EmailField(default="")
    receiver_postcode = models.CharField(max_length=10, default="")
    receiver_country = models.CharField(max_length=10, default="")
    receiver_province = models.CharField(max_length=10, default="")
    receiver_city = models.CharField(max_length=20, default="")
    receiver_district = models.CharField(max_length=20, default='')
    receiver_street = models.CharField(max_length=100, default="")
    sender_name = models.CharField(max_length=50, default="")
    sender_tel = models.CharField(max_length=20, default="")
    sender_email = models.EmailField(default="")
    sender_postcode = models.CharField(max_length=10, default="")
    sender_country = models.CharField(max_length=10, default="")
    sender_city = models.CharField(max_length=30, default="")
    sender_street = models.CharField(max_length=100, default="")
    sender_hausnr = models.CharField(max_length=10, default="")
    customer_reference_no = models.CharField(max_length=50, unique=True, blank=True,null=True)
    exporess_code = models.CharField(max_length=50, unique=True, blank=True,null=True)
    express_extra = models.TextField(default="") # 快递公司附属属性
    extra_services = models.TextField(default="") # 各种服务
    package_weight = models.FloatField(default=0, validators=[validate_decimals])
    package_goods = models.TextField(default="") # Goods
    comment = models.CharField(max_length=150, default="")
    createdtime = models.DateTimeField(auto_now_add=True)
    updatedtime = models.DateTimeField(auto_now=True)
    reserved0 = models.CharField(max_length=100, default="") #
    reserved1 = models.CharField(max_length=100, default="") #
    reserved3 = models.CharField(max_length=100, default="")
    reserved4 = models.CharField(max_length=100, default="") # extra info wie yto distribution_code
