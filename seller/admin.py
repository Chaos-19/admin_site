from decimal import Decimal
import cloudinary
from django.contrib import admin

from seller.firebase_service import set_user_role
from .models import Product, Seller
from django.contrib.admin import AdminSite

import cloudinary.uploader

from .firebase_service import add_product_to_firestore, delete_product_from_firestore


# Configuration       


# Custom Seller Admin Site
class SellerAdminSite(AdminSite):
    site_header = "Seller Dashboard"
    site_title = "Seller Administration"
    index_title = "Manage Your Products"

seller_admin_site = SellerAdminSite(name='seller_admin')



def sync_to_firestore(modeladmin, request, queryset):
    from .firebase_service import add_product_to_firestore

    def convert_decimal_to_float(data):
        """Recursively convert Decimal values to float."""
        if isinstance(data, dict):
            return {key: convert_decimal_to_float(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [convert_decimal_to_float(element) for element in data]
        elif isinstance(data, Decimal):
            return float(data)  # Convert Decimal to float
        return data
    
    print(f"Syncing {queryset.count()} products to Firestore...")
    
    for product in queryset:
        product_data = {
            'name': product.name,
            'price': float(product.price) if isinstance(product.price, Decimal) else product.price,
            'stock': float(product.stock) if isinstance(product.stock, Decimal) else product.stock,
            'description': product.description,
            'seller_id': product.seller.user.id,
            'status': product.status,
            #'product_img': product.product_img,
        }
        
        # Convert nested data if needed
        product_data = convert_decimal_to_float(product_data)
        
        # Call the Firestore service function
        add_product_to_firestore(product_data)
sync_to_firestore.short_description = "Sync selected products to Firestore"





# Product Admin for Seller Admin Site
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'status', 'price', 'stock')
    list_filter = ('status',)
    search_fields = ('name',)
    exclude = ('seller',)  # Exclude the seller field from the form
    actions = [sync_to_firestore]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superuser can see all products
        elif request.user.groups.filter(name='Sellers').exists():
            return queryset.filter(seller__user=request.user)  # Sellers see only their products
        return queryset.none()

    def save_model(self, request, obj, form, change):
        """
        Automatically associates the logged-in seller with the product being added.
        """
       
        if not change:  # Only when adding a new product
            if request.user.groups.filter(name='Sellers').exists():
                obj.seller = Seller.objects.get(user=request.user)  # Associate current user as seller
                
                
                image = form.cleaned_data.get('product_img')  
            
                if image:
                    upload_result =  cloudinary.uploader.upload(image)
                    obj.image_url = upload_result['secure_url']
                    obj.public_id = upload_result['public_id']
                    
                    
                add_product_to_firestore({
                    'name': obj.name,
                    'price': float(obj.price) if isinstance(obj.price, Decimal) else obj.price,
                    'stock': float(obj.stock) if isinstance(obj.stock, Decimal) else obj.stock,
                    'description': obj.description,
                    'seller_id': obj.seller.user.id,
                    'product_img': {
                        'url': obj.image_url,
                        'name': obj.public_id,
                    },
                    'status': obj.status,
                })
                super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superuser has change permission for all products
        if obj and request.user.groups.filter(name='Sellers').exists():
            return obj.seller.user == request.user
        return super().has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superuser has delete permission for all products
        if obj and request.user.groups.filter(name='Sellers').exists():
            return obj.seller.user == request.user
        return super().has_delete_permission(request, obj=obj)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True  # Superuser has add permission
        if request.user.groups.filter(name='Sellers').exists():
            return True
        return super().has_add_permission(request)

    # Restricting Sellers from Modifying 'Status' Field
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Sellers').exists() and not request.user.is_superuser:
            return ('status',)  # Sellers can't edit the status
        return super().get_readonly_fields(request, obj=obj)
    
    def delete_model(self, request, obj):
        # Delete from Firestore
        delete_product_from_firestore(obj.name)
        super().delete_model(request, obj)

# Product Admin for Default Admin Site
class ProductAdminForSuperAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'status', 'price', 'stock')
    list_filter = ('status',)
    search_fields = ('name',)
    
    actions = ['assign_role_to_firebase_user']

    def assign_role_to_firebase_user(self, request, queryset):
        for user in queryset:
            # Get the Firebase UID from the user model or field
            firebase_uid = user.firebase_uid  # Assuming you store the Firebase UID on the Django User model
            # Set the Firebase role (e.g., super_admin, seller_admin)
            set_user_role(firebase_uid, 'super_admin')  # or 'seller_admin'
        self.message_user(request, "Roles assigned to selected users.")

    assign_role_to_firebase_user.short_description = "Assign Firebase role to selected users"
    
    def save_model(self, request, obj, form, change):
        if not change:
            if request.user:
                obj.seller = form.cleaned_data.get('seller')
                
                image = form.cleaned_data.get('product_img')  
            
                if image:
                    upload_result =  cloudinary.uploader.upload(image)
                    obj.image_url = upload_result['secure_url']
                    obj.public_id = upload_result['public_id']
                    
                    
                add_product_to_firestore({
                    'name': obj.name,
                    'price': float(obj.price) if isinstance(obj.price, Decimal) else obj.price,
                    'stock': float(obj.stock) if isinstance(obj.stock, Decimal) else obj.stock,
                    'description': obj.description,
                    'seller_id': obj.seller.user.id,
                    'product_img': {
                        'url': obj.image_url,
                        'name': obj.public_id,
                    },
                    'status': obj.status,
                })
                super().save_model(request, obj, form, change)


# Registering with Seller Admin Site
seller_admin_site.register(Product, ProductAdmin)
seller_admin_site.register(Seller)

# Registering with Default Admin Site
admin.site.register(Product, ProductAdminForSuperAdmin)
admin.site.register(Seller)


