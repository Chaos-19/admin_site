import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
def initialize_firebase():
    try:
        # Replace 'path/to/serviceAccountKey.json' with the actual path to your Firebase Admin SDK key file
        cred = credentials.Certificate('firebase.json')
        
        # Check if Firebase is already initialized to avoid duplicate initialization
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        raise

# Function to add data to Firestore
def add_data_to_firestore(collection_name, document_id, data):
    try:
        db = firestore.client()  # Get Firestore client
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.set(data)
        print(f"Data added to collection '{collection_name}' with document ID '{document_id}'.")
    except Exception as e:
        print(f"Error adding data to Firestore: {e}")

# Main function
if __name__ == "__main__":
    # Step 1: Initialize Firebase
    initialize_firebase()

    # Step 2: Add sample data to Firestore
    # Example 1: Add a seller
    seller_data = {
        "store_name": "John's Electronics",
        "contact_info": "123-456-7890",
        "user_id": "user123",
        "email": "john@example.com",
    }
    add_data_to_firestore("sellers", "john_doe", seller_data)

    # Example 2: Add a product
    product_data = {
        "name": "Smartphone",
        "description": "Latest model with advanced features",
        "price": 699,
        "stock": 50,
        "status": "available",
        "seller_id": "user123",
    }
    add_data_to_firestore("products", "smartphone_001", product_data)
