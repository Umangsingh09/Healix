from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'address']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='patient')
    phone = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role', 'phone', 'address']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role', 'patient')
        phone = validated_data.pop('phone', '')
        address = validated_data.pop('address', '')
        validated_data.pop('password2', None)  # Remove password2 as it's not needed for user creation

        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, role=role, phone=phone, address=address)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

# SECURITY FIX: Use environment variables for passwords
# Example: password = os.getenv('DB_PASSWORD')
