from django.shortcuts import redirect, render

import seller
from .models import *

# Create your views here.

def seller_login(request):
    if request.method=='POST':
        try:
            sid= Seller.objects.get(email=request.POST['email'])
            if request.POST['password']==sid.password:
                request.session['email']=request.POST['email']
                #request.session['name']=request.POST['name']
                return render(request,'dashboard.html')
            else:
                return render(request,'seller-login.html',{'msg':'invalid password'})
        except:
            return render(request,'seller-login.html',{'msg':'email not found'})

    return render(request,'seller-login.html')

def dashboard(request):
    return render(request,'dashboard.html')
    
def add_product(request):
    if request.method=='POST':
        sellerobj =Seller.objects.get(email=request.session['email'])
        if 'pimg' in request.FILES:
            Product.objects.create(
                seller=sellerobj,
                name=request.POST['pname'],
                des=request.POST['pdes'],
                price=request.POST['pcost'],
                quantity=request.POST['pqty'],
                discount=request.POST['pdis'],
                pic=request.FILES['pimg']
            )
        else:
            Product.objects.create(
            seller=sellerobj,
            name=request.POST['pname'],
            des=request.POST['pdes'],
            price=request.POST['pcost'],
            quantity=request.POST['pqty'],
            discount=request.POST['pdis'],
            #pic=request.FILES['pimg']
        )
    return render(request,'add-product.html')

def manage_products(request):
    productlist=Product.objects.all()
    return render(request,'manage-products.html',{'productlist':productlist})

def delete_product(request,pid):
    pobj = Product.objects.get(id=pid)
    pobj.delete()
    return redirect('manage-products')

def edit_product(request,pid):
    pobj = Product.objects.get(id=pid)
    if request.method=='POST':
        pobj.name=request.POST['pname'] 
        pobj.des=request.POST['pdes'] 
        pobj.price=request.POST['pcost'] 
        pobj.quantity=request.POST['pqty']        
        pobj.discount=request.POST['pdis']
        if 'pimg' in request.FILES:
            pobj.pic=request.FILES['pimg']
        pobj.save()
        return redirect('manage-products')
        
    return render(request,'edit-product.html',{'item':pobj})