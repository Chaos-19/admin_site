from firebase_admin import firestore , auth
import firebase_admin

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url





# Ensure Firebase is initialized
if not firebase_admin._apps:
    raise ValueError("Firebase app is not initialized. Make sure to initialize the SDK by calling initialize_app().")

db = firestore.client()


def verify_firebase_token(id_token):
    """Verify the Firebase ID token."""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return None
    
def set_user_role(uid, role):
    # Assign role to a Firebase user
    auth.set_custom_user_claims(uid, {
        'role': role  # You can set 'super_admin' or 'seller_admin'
    })


def add_seller_to_firestore(seller):
    seller_ref = db.collection('sellers').document(seller.user.username)
    seller_ref.set({
        'store_name': seller.store_name,
        'contact_info': seller.contact_info,
        'user_id': seller.user.id,
        'email': seller.user.email,
    })
    print(f"Added seller '{seller.store_name}' to Firestore.")

def add_product_to_firestore(product):
    product_ref = db.collection('products').document(product['name'])
    print(product)
    product_ref.set({
        'name': product['name'],
        'description': product['description'],
        'price': product['price'],
        'stock': product['stock'],
        'status': product['status'],
        'product_img': product['product_img'],
        'seller_id': product['seller_id'],
    })
    print(f"Added product '{product['name']}' to Firestore.")
    
def delete_product_from_firestore(product_id):
    try:
        product_ref = db.collection('products').document(product_id)
        product_ref.delete()
        print(f"Product {product_id} deleted from Firestore successfully.")
    except Exception as e:
        print(f"Error deleting product {product_id} from Firestore: {e}")