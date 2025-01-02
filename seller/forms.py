# filepath: /D:/desktop/pro_ecommerce/e_commerce_admin/seller/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Product, Seller

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'status', 'price', 'stock']

class SellerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    store_name = forms.CharField(max_length=255)
    contact_info = forms.CharField(max_length=255)

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