from django.utils import timezone


from django.db import models
import datetime

# Create your models here.
class register(models.Model):
    name=models.CharField(max_length=15)
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=10,unique=True)
    password=models.CharField(max_length=10)

    def __str__(self) -> str:
        return f'{self.name}'

#join
class Join(models.Model):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=50,unique=True)
    phone=models.IntegerField()
    location=models.CharField(max_length=50)
    photo=models.FileField()
    license=models.FileField()
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    biodata=models.FileField()
    accoundnumber=models.IntegerField()
    status=models.IntegerField(default=0)
    employee_id=models.IntegerField(default=0)


class pro(models.Model):
    categorychoices=(
        ('Men','Men'),
        ('Women','Women'),
        ('Unisex','Unisex'),

    )

    name=models.CharField(max_length=50)
    image=models.ImageField()
    price=models.IntegerField()
    quantity=models.IntegerField()
    ingredients=models.CharField(max_length=300)
    netquantity=models.CharField(max_length=30)
    fragrance=models.CharField(max_length=300)
    category=models.CharField(max_length=100,default='Men',choices=categorychoices)

    def __str__(self) -> str:
        return f'{self.name}'
# class wish(models.Model):
#     user_details=models.ForeignKey(register,on_delete=models.CASCADE)
#     item_details=models.ForeignKey(pro,on_delete=models.CASCADE)
class Wishlist(models.Model):
    user_details=models.ForeignKey(register,on_delete=models.CASCADE)
    item_details=models.ForeignKey(pro,on_delete=models.CASCADE)
    date=models.CharField(max_length=30)
    status=models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.user_details.name}'




class c_rt(models.Model):
    user_det=models.ForeignKey(register,on_delete=models.CASCADE)
    pro_det=models.ForeignKey(pro,on_delete=models.CASCADE)
    status=models.IntegerField(default=0)
    date=models.CharField(max_length=30)
    cart_quantity=models.IntegerField(default=1)#buying quantity
    price=models.IntegerField()
    total_price=models.IntegerField()
    delivered = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user_det.name}'
class profile(models.Model):

    DoesNotExist = None
    user_det=models.ForeignKey(register,on_delete=models.CASCADE)
    phone=models.IntegerField()
    address=models.CharField(max_length=100)
    pincode=models.IntegerField()
    district=models.CharField(max_length=50)
    state=models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'{self.user_det.name}'
# class cart(models.Model):
#     pro_det=models.ForeignKey(pro,on_delete=models.CASCADE)
#     user_det=models.ForeignKey(register,on_delete=models.CASCADE)
#     cart_quantity=models.IntegerField(default=1)
#     total_price=models.IntegerField()


class PasswordReset(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)



# ----------ORDERS-----------


class order(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE)
    quant=models.IntegerField(default=1)
    tprice=models.FloatField()
    saddress=models.CharField(max_length=80)
    sstate=models.CharField(max_length=20)
    sdistrict=models.CharField(max_length=20)
    spincode=models.IntegerField()
    sphone=models.IntegerField()
    nname=models.CharField(default='', max_length=30)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=150, null=True, default=00000)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    updated_at = models.DateField()


    orderstatus = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )
    status = models.CharField(max_length=150, choices=orderstatus, default='pending')
    tracking_no = models.CharField(max_length=150, null=True)
    def __str__(self) -> str:
        return f'{self.tracking_no}'


class orderitem(models.Model):
    orderdet = models.ForeignKey(order, on_delete=models.CASCADE)
    product = models.ForeignKey(pro, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self) -> str:
        return f'{self.orderdet}'


