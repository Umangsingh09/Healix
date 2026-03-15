from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import UserProfile

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        import logging
        auth_logger = logging.getLogger('accounts.authentication')
        auth_logger.info(f"Authenticate called for {auth_header[:20]}...")

        id_token_str = None
        if auth_header.startswith('Bearer '):
            id_token_str = auth_header.split('Bearer ')[1]
        
        if not id_token_str:
            return None

        decoded_token = None

        try:
            import firebase_admin
            from firebase_admin import auth as firebase_auth
            
            # Initialize Firebase Admin if not already
            try:
                firebase_admin.get_app()
            except ValueError:
                firebase_admin.initialize_app(options={'projectId': 'healix-d02c4'})
            
            try:
                # verify_id_token is the recommended way for Firebase tokens
                decoded_token = firebase_auth.verify_id_token(id_token_str, check_revoked=False)
                auth_logger.info(f"Firebase Admin verified token for: {decoded_token.get('email')}")
            except Exception as admin_err:
                auth_logger.warning(f"Firebase Admin verification failed: {str(admin_err)}. Trying google-auth fallback...")
                decoded_token = id_token.verify_firebase_token(
                    id_token_str, 
                    requests.Request(), 
                    audience="healix-d02c4",
                    clock_skew_in_seconds=600 # 10 minutes tolerance
                )
                auth_logger.info("google-auth fallback successful.")
                
        except Exception as e:
            auth_logger.error(f"AUTHENTICATION FAILURE: {str(e)}")
            raise exceptions.AuthenticationFailed(f'Token Verification Failed: {str(e)}')

        if not decoded_token:
            raise exceptions.AuthenticationFailed('Invalid Firebase token')

        email = decoded_token.get('email')
        uid = decoded_token.get('sub') # Firebase UID

        if not email:
            raise exceptions.AuthenticationFailed('Email not found in token')

        # Get or create user
        user, created = User.objects.get_or_create(
            username=email,
            defaults={'email': email, 'first_name': decoded_token.get('name', '')}
        )

        # Ensure UserProfile exists and has the firebase_uid
        profile, p_created = UserProfile.objects.get_or_create(user=user)
        if p_created or profile.firebase_uid != uid:
            profile.firebase_uid = uid
            profile.save()
        
        return (user, None)
