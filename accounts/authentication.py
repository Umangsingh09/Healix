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

        id_token_str = None
        if auth_header.startswith('Bearer '):
            id_token_str = auth_header.split('Bearer ')[1]
        
        if not id_token_str:
            return None

        try:
            # Verify the Firebase ID token
            # Note: audience should be your Firebase Project ID
            decoded_token = id_token.verify_firebase_token(
                id_token_str, 
                requests.Request(), 
                audience="healix-d02c4"
            )
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Invalid Firebase token: {str(e)}')

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
