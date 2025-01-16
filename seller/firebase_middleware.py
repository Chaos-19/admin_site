from django.http import HttpResponseForbidden
from .firebase_service import verify_firebase_token

class FirebaseAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is accessing the admin panel
        if request.path.startswith('/admin/'):
            id_token = request.META.get('HTTP_AUTHORIZATION')  # Get token from Authorization header
            
            if id_token:
                # Verify the Firebase token
                decoded_token = verify_firebase_token(id_token)
                
                if decoded_token:
                    # Get the role of the user from Firebase claims or the token
                    role = decoded_token.get('role', '')
                    
                    # Check if the user has the necessary role to access the admin panel
                    if role in ['super_admin', 'seller_admin']:
                        # User is authorized, continue the request
                        pass
                    else:
                        return HttpResponseForbidden("You are not authorized to access the admin panel.")
                else:
                    return HttpResponseForbidden("Invalid Firebase token.")
            else:
                return HttpResponseForbidden("Authorization token missing.")
        
        # Process the request
        response = self.get_response(request)
        return response
