from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.PositiveBigIntegerField()
    address=models.TextField()
    password=models.CharField(max_length=100)
    profile_picture=models.ImageField(default="",upload_to="profile_picture/")
    usertype=models.CharField(max_length=100,default="buyer")

    def __str__(self):
        return self.fname
    
class Product(models.Model):

    category=(
                ("Men","Men"),
                ("Women","Women"),
                ("kids","kids"),
            )
    brand=(
                ("Raymond","Raymond"),
                ("U.S. Polo Assn.","U.S. Polo Assn."),
                ("Peter England","Peter England"),
                ("Chanel","Chanel"),
                ("Calvin Klein","Calvin Klein"),
                ("Nike","Nike"),
            )
    size=(
                ("XS","XS"),
                ("S","S"),
                ("M","M"),
                ("L","L"),
                ("XL","XL"),
                ("XXL","XXL"),
                ("FREE SIZE","FREE SIZE"),
            )
    seller=models.ForeignKey(User,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_price=models.PositiveIntegerField(default=10)
    product_category=models.CharField(max_length=100,choices=category)
    product_brand=models.CharField(max_length=100,choices=brand)
    product_size=models.CharField(max_length=100,choices=size)
    product_image=models.ImageField(upload_to="product_images/")
    product_desc=models.TextField()

    def __str__(self):
        return self.seller.fname+" - "+self.product_name
    
class Wishlist(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.buyer.fname+" - "+self.product.product_name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    product_price=models.PositiveIntegerField()
    product_qty=models.PositiveIntegerField(default=1)
    total_price=models.PositiveIntegerField()
    payment_status=models.BooleanField(default=False)

    def __str__(self):
        return self.user.fname+" - "+self.product.product_name