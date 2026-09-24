from rest_framework import serializers
from .models import *
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    phone = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True) 
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        if not value:
            raise serializers.ValidationError("Refresh token is required.")
        return value
    