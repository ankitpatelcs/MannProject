
from datetime import datetime
from random import randrange
from django.http import JsonResponse,HttpResponseBadRequest
from django.shortcuts import redirect, render

from seller.models import *
from .models import *

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import send_mail


# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def register(request):
    if request.method=='POST':
        try:
            userobj=User.objects.get(email=request.POST['email'])
            return render(request,'register.html',{'msg':'Email Already Registered'})
        except:
            if request.POST['password'] == request.POST['cnfpassword']:
                #global otp
                otp = str(randrange(1000,9999))
                subject = 'OTP for Registration'
                message = f'The OTP for registration of your email is {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'otp.html',{'otp':otp,'email':request.POST['email'],'name':request.POST['name'],'password':request.POST['password']})            
                
            else:
                return render(request,'register.html',{'msg':'Passwords do not match'})
    return render(request,'register.html')

def otp(request):
    if request.method=='POST':
        if request.POST['hiddenotp']==request.POST['otp']:        
            User.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            return render(request,'register.html',{'msg':'Success'})
        
        return render(request,'otp.html',{'msg':'Wrong OTP'})    

def login(request):
    if request.method=='POST':
        try:
            uid= User.objects.get(email=request.POST['email'])
            if uid.password==request.POST['password']:
                request.session["UserName"]=uid.name
                request.session["UserId"]=uid.id
                return redirect('index')
            else:
                return render(request,'login.html',{'msg':'password do not match'})
        except:
            return render(request,'login.html',{'msg':'Email not found'})
    return render(request,'login.html')

def products(request):
    plist = Product.objects.all()
    return render(request,'products.html',{'productlist':plist})

def single(request,pid):
    pobj = Product.objects.get(id=pid)    
    return render(request,'single.html',{'item':pobj})

def add_to_cart(request):
    pid=request.GET['pid']
    userobj = User.objects.get(id=request.session['UserId'])
    pobj = Product.objects.get(id=pid)
    Cart.objects.create(
        user=userobj,
        product=pobj,
        quantity=1
    )    
    return JsonResponse({'msg':'Addded into Cart'})

def cart(request):
    userobj = User.objects.get(id=request.session['UserId'])
    cartdata = Cart.objects.filter(user=userobj)
    return render(request,'cart.html',{'cartitems':cartdata})

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def pay(request):
    userobj= User.objects.get(id=request.session["UserId"])
    orderobj = Order.objects.create(
        user=userobj,
        orderdate=datetime.now().strftime ("%Y-%m-%d"),
        orderstatus='confirm'
    )
    
    cart = Cart.objects.filter(user=userobj)
    TotalCost = 0
    for i in cart:        
        TotalCost +=  int(i.product.price)

    for item in cart:
        OrderDetails.objects.create(
            product=item.product,
            quantiy=item.quantity,
            order=orderobj
        )

    currency = 'INR'
    amount = TotalCost*100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = f'paymenthandler/{orderobj.id}'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request,'pay.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'success.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'fail.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'fail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()