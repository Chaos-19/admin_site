# filepath: /D:/desktop/pro_ecommerce/e_commerce_admin/seller/firebase_service.py
import firebase_admin
from firebase_admin import firestore

db = firestore.client()

def add_seller_to_firestore(seller):
    seller_ref = db.collection('sellers').document(seller.user.username)
    seller_ref.set({
        'store_name': seller.store_name,
        'contact_info': seller.contact_info,
        'user_id': seller.user.id,
        'email': seller.user.email,
    })

def add_product_to_firestore(product):
    product_ref = db.collection('products').document(product.name)
    product_ref.set({
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'status': product.status,
        'seller_id': product.seller.user.id,
    })