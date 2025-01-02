from django.contrib import admin
from django.urls import path, include
from seller.admin import seller_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('seller-admin/', seller_admin_site.urls),  # Custom seller admin site
    path('seller/', include('seller.urls')),  # Include seller URLs
]
