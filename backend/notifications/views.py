from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from notifications.services.notification_service import (
    NotificationService
)


from .models import (
    NotificationTrigger,
    NotificationTemplate,
)

from .serializers import (
    NotificationTriggerSerializer,
    NotificationTemplateSerializer,
)
# Register User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
                    
# ============================================================
# NOTIFICATION TRIGGER APIs
# ============================================================


class NotificationTriggerListAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):

        triggers = NotificationTrigger.objects.all()

        serializer = NotificationTriggerSerializer(
            triggers,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class NotificationTriggerCreateAPIView(APIView):
    permission_classes = [IsAdminUser]


    def post(self, request):

        serializer = NotificationTriggerSerializer(
            data=request.data
        )

        if serializer.is_valid():
            trigger = serializer.save()

            return Response(
                NotificationTriggerSerializer(trigger).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class NotificationTriggerDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        try:
            trigger = NotificationTrigger.objects.get(pk=pk)

        except NotificationTrigger.DoesNotExist:
            return Response(
                {
                    "message": "Trigger not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NotificationTriggerSerializer(trigger)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class NotificationTriggerUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        try:
            trigger = NotificationTrigger.objects.get(pk=pk)

        except NotificationTrigger.DoesNotExist:
            return Response(
                {
                    "message": "Trigger not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NotificationTriggerSerializer(
            trigger,
            data=request.data
        )

        if serializer.is_valid():
            trigger = serializer.save()

            return Response(
                NotificationTriggerSerializer(trigger).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class NotificationTriggerPatchAPIView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        try:
            trigger = NotificationTrigger.objects.get(pk=pk)

        except NotificationTrigger.DoesNotExist:
            return Response(
                {
                    "message": "Trigger not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NotificationTriggerSerializer(
            trigger,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            trigger = serializer.save()

            return Response(
                NotificationTriggerSerializer(trigger).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class NotificationTriggerDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        try:
            trigger = NotificationTrigger.objects.get(pk=pk)

        except NotificationTrigger.DoesNotExist:
            return Response(
                {
                    "message": "Trigger not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        trigger.delete()

        return Response(
            {
                "message": "Trigger deleted successfully."
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# NOTIFICATION TEMPLATE APIs
# ============================================================


class NotificationTemplateListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        templates = NotificationTemplate.objects.select_related(
            "trigger"
        ).all()

        serializer = NotificationTemplateSerializer(
            templates,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class NotificationTemplateCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = NotificationTemplateSerializer(
            data=request.data
        )

        if serializer.is_valid():
            template = serializer.save()

            return Response(
                NotificationTemplateSerializer(template).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class NotificationTemplateDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        try:
            template = NotificationTemplate.objects.select_related(
                "trigger"
            ).get(pk=pk)

        except NotificationTemplate.DoesNotExist:
            return Response(
                {
                    "message": "Template not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NotificationTemplateSerializer(template)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class NotificationTemplateUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        try:
            template = NotificationTemplate.objects.get(pk=pk)

        except NotificationTemplate.DoesNotExist:
            return Response(
                {
                    "message": "Template not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NotificationTemplateSerializer(
            template,
            data=request.data
        )

        if serializer.is_valid():
            template = serializer.save()

            return Response(
                NotificationTemplateSerializer(template).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class NotificationTemplatePatchAPIView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        try:
            template = NotificationTemplate.objects.get(pk=pk)

        except NotificationTemplate.DoesNotExist:
            return Response(
                {
                    "message": "Template not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NotificationTemplateSerializer(
            template,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            template = serializer.save()

            return Response(
                NotificationTemplateSerializer(template).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class NotificationTemplateDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        try:
            template = NotificationTemplate.objects.get(pk=pk)

        except NotificationTemplate.DoesNotExist:
            return Response(
                {
                    "message": "Template not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        template.delete()

        return Response(
            {
                "message": "Template deleted successfully."
            },
            status=status.HTTP_200_OK
        )