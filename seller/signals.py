from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .firebase_service import add_product_to_firestore
from decimal import Decimal

# Helper function to handle Decimal to float conversion
def convert_decimal_to_float(data):
    """Recursively convert Decimal values to float."""
    if isinstance(data, dict):
        return {key: convert_decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_decimal_to_float(element) for element in data]
    elif isinstance(data, Decimal):
        return float(data)  # Convert Decimal to float
    return data

# Signal handler to sync product to Firestore when a new product is saved
@receiver(post_save, sender=Product)
def sync_product_to_firestore(sender, instance, created, **kwargs):
    if created: 
        product_data = {
            'name': instance.name,
            'price': float(instance.price) if isinstance(instance.price, Decimal) else instance.price,
            'stock': float(instance.stock) if isinstance(instance.stock, Decimal) else instance.stock,
            'description': instance.description,
            'seller_id': instance.seller.user.id,
            'product_img': {
                'url': instance.image_url,
                'name': instance.public_id,
            },
            'status': instance.status,
        }

        # Convert any Decimal fields if necessary
        product_data = convert_decimal_to_float(product_data)
        
        print("in signal method .....")
        
        #add_product_to_firestore(product_data)
