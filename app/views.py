from unicodedata import category
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        accessories = Product.objects.filter(category='AC')
        smartphones = Product.objects.filter(category='S')
        laptops = Product.objects.filter(category='L')
        earphones = Product.objects.filter(category='E')
        others = Product.objects.filter(category='O')
        dealsofday = Product.objects.filter(category='DD')
        dealsofdaysecond = Product.objects.filter(category='dd')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'accessories':accessories, 'smartphones':smartphones, 'laptops':laptops, 'earphones':earphones, 'others':others, 'dealsofday':dealsofday, 'dealsofdaysecond':dealsofdaysecond, 'totalitem':totalitem})

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount': totalamount, 'amount':amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET ['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET ['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
            'amount': amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)




def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op, 'totalitem':totalitem})

def smartphone(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        smartphone = Product.objects.filter(category='S')
    elif data in ['oppo', 'Apple', 'Samsung', 'vivo', 'Nokia']:
        smartphone = Product.objects.filter(category='S').filter(brand=data)
    elif data == "below":
        smartphone = Product.objects.filter(category='S').filter(discounted_price__lt=10000)
    elif data == "below2":
        smartphone = Product.objects.filter(category='S').filter(discounted_price__lt=20000)
    elif data == "above":
        smartphone = Product.objects.filter(category='S').filter(discounted_price__gt=20000)
    return render(request, 'app/smartphone.html', {'smartphone':smartphone, 'totalitem':totalitem})

def laptop(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data in ['ASUS', 'Aser', 'HP', 'Lenovo', 'Apple']:
        laptop = Product.objects.filter(category='L').filter(brand=data)
    elif data == "below":
        laptop = Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    elif data == "below2":
        laptop = Product.objects.filter(category='L').filter(discounted_price__lt=70000)
    elif data == "above":
        laptop = Product.objects.filter(category='L').filter(discounted_price__gt=70000)
    return render(request, 'app/laptop.html', {'laptop':laptop, 'totalitem':totalitem})

def earphone(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        earphone = Product.objects.filter(category='E')
    elif data in ['Bose', 'Boat', 'boat', 'JBL', 'Apple', 'Sony', 'Jabra']:
        earphone = Product.objects.filter(category='E').filter(brand=data)
    elif data == "below":
        earphone = Product.objects.filter(category='E').filter(discounted_price__lt=5000)
    elif data == "below2":
        earphone = Product.objects.filter(category='E').filter(discounted_price__lt=10000)
    elif data == "above":
        earphone = Product.objects.filter(category='E').filter(discounted_price__gt=10000)
    return render(request, 'app/earphone.html', {'earphone':earphone, 'totalitem':totalitem})

def other(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        other = Product.objects.filter(category='O')
    elif data in ['JBL', 'Logitech', 'ASUS', 'Philips', 'Apple', 'Sony', 'HP', 'Samsung', 'LG', 'Applw', 'Bajaj', 'Canon']:
        other = Product.objects.filter(category='O').filter(brand=data)
    elif data == "below":
        other = Product.objects.filter(category='O').filter(discounted_price__lt=5000)
    elif data == "below2":
        other = Product.objects.filter(category='O').filter(discounted_price__lt=10000)
    elif data == "below3":
        other = Product.objects.filter(category='O').filter(discounted_price__lt=20000)
    elif data == "below4":
        other = Product.objects.filter(category='O').filter(discounted_price__lt=35000)
    elif data == "above":
        other = Product.objects.filter(category='O').filter(discounted_price__gt=10000)
    return render(request, 'app/other.html', {'other':other, 'totalitem':totalitem})

def topwear(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        topwear = Product.objects.filter(category='TW')
    elif data in ['Arrow', 'PeterEngland', 'Raymonds', 'VanHeusen', 'Armani', 'JacJones', 'Spykar', 'Levis', 'HM', 'USpolo']:
        topwear = Product.objects.filter(category='TW').filter(brand=data)
    elif data == "below":
        topwear = Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
    elif data == "below2":
        topwear = Product.objects.filter(category='TW').filter(discounted_price__lt=2000)
    elif data == "below3":
        topwear = Product.objects.filter(category='TW').filter(discounted_price__lt=3000)
    elif data == "above":
        topwear = Product.objects.filter(category='TW').filter(discounted_price__gt=3000)
    return render(request, 'app/topwear.html', {'topwear':topwear, 'totalitem':totalitem})

def bottomwear(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        bottomwear = Product.objects.filter(category='BW')
    elif data in ['ReDone', 'Frame', 'Gap', 'Everlane',  'Levis']:
        bottomwear = Product.objects.filter(category='BW').filter(brand=data)
    elif data == "below":
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
    elif data == "below2":
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=2000)
    elif data == "below3":
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=3000)
    elif data == "above":
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gt=3000)
    return render(request, 'app/bottomwear.html', {'bottomwear':bottomwear, 'totalitem':totalitem})

def accessories(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        accessories = Product.objects.filter(category='AC')
    elif data in ['Woodland', '705', 'Trail', 'NBL', 'Bloglow', 'Raymonds', 'RAY-BAN', 'Loreal', 'OPI', 'COCO', 'Vlrsace', 'ParkAvenue', 'COCOOIL', 'Natchu', 'Nike', 'Jordan', 'puma', 'Tissot', 'IOC', 'Fossil', 'Addidas']:
        accessories = Product.objects.filter(category='AC').filter(brand=data)
    elif data == "below":
        accessories = Product.objects.filter(category='AC').filter(discounted_price__lt=1000)
    elif data == "below2":
        accessories = Product.objects.filter(category='AC').filter(discounted_price__lt=2000)
    elif data == "below3":
        accessories = Product.objects.filter(category='AC').filter(discounted_price__lt=3000)
    elif data == "below4":
        accessories = Product.objects.filter(category='AC').filter(discounted_price__lt=5000)
    elif data == "below5":
        accessories = Product.objects.filter(category='AC').filter(discounted_price__lt=10000)
    elif data == "above":
        accessories = Product.objects.filter(category='AC').filter(discounted_price__gt=10000)
    return render(request, 'app/accessories.html', {'accessories':accessories, 'totalitem':totalitem})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'totalitem':totalitem})

@login_required
def payment_done(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, state=state, city=city, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation!! Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})