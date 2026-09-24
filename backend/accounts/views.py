from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
import random
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from notifications.services.notification_service import NotificationService
# Create your views here.

class RegisterAPIView(APIView):

    def post(self, request):
        print("Requested Data:", request.data)

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        email = data["email"]
        password = data["password"]

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {
                    "error": "User with this email already exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate unique username
        base_name = data.get("first_name", "user").lower()
        user_name = f"{base_name}_{random.randint(100000, 999999)}"

        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            user_name=user_name,
            phone=data.get("phone"),
        )

        return Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_name": user.user_name,
                    "phone": user.phone,
                }
            },
            status=status.HTTP_201_CREATED
        )
        
        
class LoginAPIView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(email=email, password=password)
        if not user:
            return Response({"error": "Invalid login credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        print("Last Step for login")
        # Send login notification
        notification_result = NotificationService.send_notification(
            trigger_code="LOGIN",

            email=user.email,

            phone_number=user.phone,

            variables={
                "user_name": user.user_name,
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "email": user.email,
            }
        )
        print("notification_result",notification_result)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": "Login successful"
        })



class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "error": "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            token = RefreshToken(refresh_token)

            # Blacklist refresh token
            token.blacklist()

        except Exception:
            return Response(
                {
                    "error": "Invalid or expired refresh token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Send logout notification
        notification_result = NotificationService.send_notification(
            trigger_code="USER_LOGOUT",

            email=user.email,

            phone_number=user.phone,

            variables={
                "user_name": user.user_name,
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "email": user.email,
            }
        )

        return Response(
            {
                "message": "Logout successful",
                "notification": notification_result
            },
            status=status.HTTP_200_OK
        )          