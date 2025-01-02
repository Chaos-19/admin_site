from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from .models import Product, Seller
from .forms import ProductForm, SellerRegistrationForm
from django.contrib.auth.decorators import login_required

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = Seller.objects.get(user=request.user)
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'seller/add_product.html', {'form': form})

@login_required
def view_products(request):
    seller = Seller.objects.get(user=request.user)
    products = Product.objects.filter(seller=seller)
    return render(request, 'seller/view_products.html', {'products': products})

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            user = seller.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            seller.save()
            # Add the user to the 'Sellers' group
            sellers_group, created = Group.objects.get_or_create(name='Sellers')
            user.groups.add(sellers_group)
            # Grant staff permissions
            user.is_staff = True
            user.save()
            # Redirect to admin site login page
            return redirect('/seller-admin/login/')
    else:
        form = SellerRegistrationForm()
    return render(request, 'seller/register.html', {'form': form})
