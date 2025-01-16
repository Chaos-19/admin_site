import firebase_admin
from firebase_admin import auth
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Assign a custom role (super_admin or seller_admin) to a Firebase user'

    def add_arguments(self, parser):
        # Allow passing the user ID and role from the command line
        parser.add_argument('uid', type=str, help='The Firebase User ID (UID)')
        parser.add_argument('role', type=str, choices=['super_admin', 'seller_admin'], help='Role to assign to the user')

    def handle(self, *args, **kwargs):
        uid = kwargs['uid']
        role = kwargs['role']
        
        try:
            # Assign the custom role claim to the Firebase user
            auth.set_custom_user_claims(uid, {'role': role})
            self.stdout.write(self.style.SUCCESS(f'Successfully assigned {role} to user {uid}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error assigning role: {e}'))
