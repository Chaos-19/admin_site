# filepath: /D:/desktop/pro_ecommerce/e_commerce_admin/seller/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Product, Seller

class ProductForm(forms.ModelForm):
    product_img = forms.ImageField(required=False, label="Upload Image")
    
    class Meta:
        model = Product
        fields = ['name', 'status', 'price', 'stock', 'product_img']

class SellerRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': 'Email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': 'Password'
        })
    )
    store_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': 'Store Name'
            
        })
    )
    contact_info = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': 'Contact Info'
        })
    )

    class Meta:
        model = Seller
        fields = ['username', 'password', 'email', 'store_name', 'contact_info']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )
        seller = Seller(
            user=user,
            store_name=self.cleaned_data['store_name'],
            contact_info=self.cleaned_data['contact_info']
        )
        if commit:
            user.save()
            seller.save()
        return seller