from django.shortcuts import render,redirect
from .models import User,Product,Wishlist,Cart
from django.contrib.auth.hashers import make_password, check_password
import requests
import random

# Create your views here.
def index(request):
    try:
        user=User.objects.get(email=request.session['email'])
        if user.usertype=="buyer":
            return render(request,'index.html')
        else:
            return render(request,'seller-index.html')
    except:
        return render(request,'index.html')
    
def seller_index(request):
    return render(request,'seller-index.html')

def product(request,cat):
    products=Product()
    if cat=="all":
        products=Product.objects.all()
    elif cat=="women":
        products=Product.objects.filter(product_category="Women")
    elif cat=="men":
        products=Product.objects.filter(product_category="Men")
    elif cat=="kids":
        products=Product.objects.filter(product_category="kids")
    return render(request,'product.html',{'products':products})

def shoping_cart(request):
    return render(request,'shoping-cart.html')

def blog(request):
    return render(request,'blog.html')


def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                print("Password...............",make_password(request.POST['password']))
                User.objects.create(
                        usertype=request.POST['usertype'],
                        fname=request.POST['fname'],
                        lname=request.POST['lname'],
                        email=request.POST['email'],
                        mobile=request.POST['mobile'],
                        address=request.POST['address'],
                        password=make_password(request.POST['password']),
                        profile_picture=request.FILES["profile_picture"],
                    )
                msg="User Sign Up Successfully"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Does Not Matched"
                return render(request,'signup.html',{'msg':msg})
    else:           
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            checkpassword=check_password(request.POST['password'],user.password)
            if checkpassword==True:
                if user.usertype=="buyer":
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    request.session['profile_picture']=user.profile_picture.url
                    wishlists=Wishlist.objects.filter(buyer=user)
                    carts=Cart.objects.filter(user=user)
                    request.session['wishlist_count']=len(wishlists)
                    request.session['cart_count']=len(carts)
                    return render(request,'index.html') 
                else:
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    request.session['profile_picture']=user.profile_picture.url
                    return render(request,'seller-index.html') 
            else:
                msg="Password In Incorrect"
                return render(request,'login.html',{'msg':msg})
        except:
            return render(request,'login.html',{'msg':'Email Is Incorrect'})
    else:
        return render(request,'login.html')
    
def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        del request.session['profile_picture']
        del request.session['wishlist_count']
        del request.session['cart_count']
        return render(request,'login.html')
    except:
        return render(request,'login.html')
    
def forgot_password(request):
    if request.method=="POST":
        try:
            otp=random.randint(10000,9999)
            user=User.objects.get(mobile=request.POST['mobile'])
            mobile=request.POST['mobile']
            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {"authorization":"YOUR_API_KEY","variables_values":str(otp),"route":"otp","numbers":"mobile"}
            headers = {'cache-control': "no-cache"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            request.session['mobile']=mobile
            request.session['otp']=otp
            return render(request,'otp.html')
        except:
            msg="Mobile Number Is Not Registered"
            return render(request,'forgot-password.html',{'msg':msg})
    else:
        return render(request,'forgot-password.html')
    
def verify_otp(request):
    otp=int(request.session['otp'])
    uotp=int(request.POST['uotp'])
    print(otp)
    print(uotp)
    if otp==uotp:
        del request.session['otp']
        return render(request,'new-password.html')
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'msg':msg})
    
def new_password(request):
    if request.POST['new_password']==request.POST['cnew_password']:
        mobile=request.session['mobile']
        user=User.objects.get(mobile=mobile)
        user.password=make_password(request.POST['new_password'])
        user.save()
        return redirect('logout')
    else:
        msg="New Password & Confirm New Password Does Not Matched"
        return render(requests,'new-password.html',{'msg':msg})
    
def change_password(request):
    email=request.session['email']
    user=User.objects.get(email=email)
    if request.method=="POST":
        check_password=check_password(request.POST['old_password'],user.password)
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=make_password(request.POST['new_password'])
                user.save()
                return redirect('logout')
            else:
                msg="New Password & Confirm New Password Does Not Matched"
                if user.usertype=="buyer":
                    return render(request,'change-password.html',{'msg':msg})
                else:
                    return render(request,'seller-change-password.html',{'msg':msg})
        else:
            msg="Old Password Does Not Matched"
            if user.usertype=="buyer":
                return render(request,'change-password.html',{'msg':msg})
            else:
                return render(request,'seller-change-password.html',{'msg':msg})
    else:
        if user.usertype=="buyer":
            return render(request,'change-password.html')
        else:
            return render(request,'seller-change-password.html')
    
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        try:
            user.profile_picture=request.FILES['profile_picture']
        except:
            pass
        user.save()
        request.session['profile_picture']=user.profile_picture.url
        msg="Profile Updated Successfull"
        if user.usertype=="buyer":
            return render(request,'profile.html',{'user':user,'msg':msg})
        else:
            return render(request,'seller-profile.html',{'user':user,'msg':msg})
    else:
        if user.usertype=="buyer":
            return render(request,'profile.html',{'user':user})
        else:
            return render(request,'seller-profile.html',{'user':user})
        
def seller_add_product(request):
    seller=User.objects.get(email=request.session['email'])

    if request.method=="POST":
        Product.objects.create(
                seller=seller,
                product_category=request.POST['product_category'],
                product_brand=request.POST['product_brand'],
                product_size=request.POST['product_size'],
                product_name=request.POST['product_name'],
                product_price=request.POST['product_price'],
                product_desc=request.POST['product_desc'],
                product_image=request.FILES['product_image'],
            )
        msg="Product Added Successfully"
        return render(request,'seller-add-product.html',{'msg':msg})
    else:
        return render(request,'seller-add-product.html')
    
def seller_view_product(request):
    seller=User.objects.get(email=request.session['email'])
    product=Product.objects.filter(seller=seller)
    return render(request,'seller-view-product.html',{'product': product})

def seller_product_details(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'seller-product-details.html',{'product': product})

def seller_product_edit(request,pk):
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
        product.product_category=request.POST['product_category']
        product.product_brand=request.POST['product_brand']
        product.product_name=request.POST['product_name']
        product.product_desc=request.POST['product_desc']
        product.product_price=request.POST['product_price']
        product.product_size=request.POST['product_size']
        try:
            product.product_image=request.FILES['product_image']
        except:
            pass
        product.save()
        msg="Product Updated Successfully"
        return render(request,'seller-product-edit.html',{'product': product,'msg':msg})
    else:
        return render(request,'seller-product-edit.html',{'product': product})
    
def seller_product_delete(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect("seller-view-product")

def product_details(request,pk):
    wishlist_flag=False
    cart_flag=False
    buyer=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    try:
        Wishlist.objects.get(buyer=buyer,product=product)
        wishlist_flag=True
    except:
        pass
    if  Cart.objects.filter(user=buyer,product=product).exists():
        cart_flag=True
    return render(request,'product-details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})
    
def wishlist(request,pk):
    buyer=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    Wishlist.objects.create(buyer=buyer,product=product)
    return redirect('my-favourite')

def my_favourite(request):
    buyer=User.objects.get(email=request.session['email'])
    wishlists=Wishlist.objects.filter(buyer=buyer)
    request.session['wishlist_count']=len(wishlists)
    return render(request,"wishlist.html",{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
    buyer=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    wishlist=Wishlist.objects.get(buyer=buyer,product=product)
    wishlist.delete()
    return redirect('my-favourite')

def add_to_cart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    product_qty = 1
    total_price=product.product_price * product_qty
    if not Cart.objects.filter(user=user,product=product).exists():
        Cart.objects.create(
            user=user,
            product=product,
            product_price=product.product_price,
            product_qty=product_qty,
            total_price=total_price,
                            )
        cart_count=Cart.objects.filter(user=user).count()
        request.session['cart_count']=cart_count
        cart_flag=False
        try:
            Cart.objects.get(user=user,product=product)
            cart_flag=True
        except:
            pass
        return render(request,'product-details.html',{'product':product,'cart_flag':cart_flag})
    else:
        cart_flag=False
        try:
            Cart.objects.get(user=user,product=product)
            cart_flag=True
        except:
            pass
        return render(request,'product-details.html',{'product':product,'cart_flag':cart_flag})


def shoping_cart(request):
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user)
    sub_price=sum(carts.values_list('total_price', flat=True))
    return render(request,"shoping-cart.html",{'carts':carts,'sub_price':sub_price})

def cart_qty(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    carts=Cart.objects.get(user=user,product=product)

    carts.product_qty +=1
    carts.total_price=carts.product_qty*product.product_price
    carts.save()
    return redirect('shoping-cart')

def cart_qty_minus(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    carts=Cart.objects.get(user=user,product=product)

    carts.product_qty -=1
    carts.total_price=carts.product_qty*product.product_price
    carts.save()
    return redirect('shoping-cart')