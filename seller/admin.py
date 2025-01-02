'''from django.contrib import admin
from .models import Product, Seller
from django.contrib.admin import AdminSite

# Custom Seller Admin Site
class SellerAdminSite(AdminSite):
    site_header = "Seller Dashboard"
    site_title = "Seller Administration"
    index_title = "Manage Your Products"

seller_admin_site = SellerAdminSite(name='seller_admin')

# Product Admin for Seller Admin Site
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'status', 'price', 'stock')
    list_filter = ('status',)
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superuser can see all products
        elif request.user.groups.filter(name='Sellers').exists():
            return queryset.filter(seller__user=request.user)  # Sellers see only their products
        return queryset.none()

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

    def save_model(self, request, obj, form, change):
        if not obj.seller_id and request.user.groups.filter(name='Sellers').exists():
            obj.seller = Seller.objects.get(user=request.user)  # Automatically assign seller
        super().save_model(request, obj, form, change)

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

# Product Admin for Default Admin Site
class ProductAdminForSuperAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'status', 'price', 'stock')
    list_filter = ('status',)
    search_fields = ('name',)

# Registering with Seller Admin Site
seller_admin_site.register(Product, ProductAdmin)
seller_admin_site.register(Seller)

# Registering with Default Admin Site
admin.site.register(Product, ProductAdminForSuperAdmin)
admin.site.register(Seller)
'''
from django.contrib import admin
from .models import Product, Seller
from django.contrib.admin import AdminSite

# Custom Seller Admin Site
class SellerAdminSite(AdminSite):
    site_header = "Seller Dashboard"
    site_title = "Seller Administration"
    index_title = "Manage Your Products"

seller_admin_site = SellerAdminSite(name='seller_admin')








# Product Admin for Seller Admin Site
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'status', 'price', 'stock')
    list_filter = ('status',)
    search_fields = ('name',)
    exclude = ('seller',)  # Exclude the seller field from the form

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

# Product Admin for Default Admin Site
class ProductAdminForSuperAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'status', 'price', 'stock')
    list_filter = ('status',)
    search_fields = ('name',)

# Registering with Seller Admin Site
seller_admin_site.register(Product, ProductAdmin)
seller_admin_site.register(Seller)

# Registering with Default Admin Site
admin.site.register(Product, ProductAdminForSuperAdmin)
admin.site.register(Seller)
