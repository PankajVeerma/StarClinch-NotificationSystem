from rest_framework import serializers
from .models import (
    NotificationTrigger,
    NotificationTemplate,
)

class NotificationTriggerSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationTrigger
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class NotificationTemplateSerializer(serializers.ModelSerializer):

    trigger_name = serializers.CharField(
        source="trigger.name",
        read_only=True
    )

    class Meta:
        model = NotificationTemplate
        fields = "__all__"
        read_only_fields = [
            "id",
            "trigger_name",
            "created_at",
            "updated_at",
        ]