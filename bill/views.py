from rest_framework import viewsets
from django.shortcuts import render,redirect,get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from .models import Product
from django.http import HttpResponse  
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def Home(request):
   return redirect("/login") 

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(username,password)
        if user is not None:
            login(request,user) 
            print(user,password)
            # Redirect to a success page or wherever you want
            return redirect('/list/')  # Assuming 'dashboard' is the name of your dashboard URL
        else:
            # Return an invalid login message or handle the error as needed
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')   
    

def show(request):
    data=Product.objects.all()
    return render(request,"ShowProduct.html",{"data":data})     



def update_product(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
            return render(request, 'update_product.html', {'product': product})
        except Product.DoesNotExist:
            return HttpResponse("Product does not exist.")

    elif request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description') 
        product = Product.objects.get(id=product_id)   
        product.name = name
        product.price = price
        product.description = description
        product.save()
        return redirect('/list')

def delete_product(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return redirect('/list/')  
        except Product.DoesNotExist:
            return HttpResponse("Product does not exist.")
    

def add_product(request):
    if request.method == 'GET':
        # Render the add product form
        return render(request, 'add_product.html')
    elif request.method == 'POST':
        # Create a new product based on the form submission
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        
        product = Product.objects.create(name=name, price=price, description=description)

        return redirect('/list/')
    


def bill_generator(request):
    if request.method == 'GET':
        # Fetch all products to populate the select dropdown
        products = Product.objects.all()
        return render(request, 'bill_generator.html', {'products': products})
    elif request.method == 'POST':
        # Calculate the total price of selected products
        selected_product_ids = request.POST.getlist('products')
        total_price = 0
        selected_products = []
        for product_id in selected_product_ids:
            product = Product.objects.get(id=product_id)
            total_price += product.price
            selected_products.append(product)
             
        # Render the bill with the selected products and total price
        return render(request, 'bill.html', {'products': selected_products, 'total_price': total_price})      
    



def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/list/')
         
          # Assuming 'dashboard' is the name of your dashboard URL
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
