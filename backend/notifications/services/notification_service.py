from django.utils import timezone

from notifications.models import (
    NotificationTrigger,
    NotificationTemplate,
)

from .template_service import TemplateService
from .email_service import EmailService
from .whatsapp_service import WhatsAppService
from .push_service import PushService


class NotificationService:

    @staticmethod
    def send_notification(
        trigger_code,
        email=None,
        phone_number=None,
        push_subscription=True,
        variables=None,
    ):
        if variables is None:
            variables = {}

        trigger = NotificationTrigger.objects.filter(
            code=trigger_code,
            is_active=True
        ).first()
        print("Trigger====",trigger)
        if not trigger:
            return {
                "success": False,
                "message": "Trigger not found or inactive."
            }

        templates = NotificationTemplate.objects.filter(
            trigger=trigger,
            is_active=True
        )

        results = []

        for template in templates:

            subject = TemplateService.render(
                template.subject,
                variables
            )

            body = TemplateService.render(
                template.body,
                variables
            )

            if template.channel == NotificationTemplate.Channel.EMAIL:

                if not email:
                    results.append({
                        "channel": "EMAIL",
                        "success": False,
                        "message": "Email not provided."
                    })
                    continue
                    print("===========")
                result = EmailService.send_email(
                    to_email=email,
                    subject=subject,
                    body=body
                )

                results.append(result)

            elif template.channel == NotificationTemplate.Channel.WHATSAPP:

                if not phone_number:
                    results.append({
                        "channel": "WHATSAPP",
                        "success": False,
                        "message": "Phone number not provided."
                    })
                    continue

                result = WhatsAppService.send_message(
                    phone_number=phone_number,
                    message=body
                )

                results.append(result)

            elif template.channel == NotificationTemplate.Channel.WEB_PUSH:

                if not push_subscription:
                    results.append({
                        "channel": "WEB_PUSH",
                        "success": False,
                        "message": "Push subscription not provided."
                    })
                    continue

                result = PushService.send_push(
                    subscription=push_subscription,
                    title=subject,
                    body=body
                )

                results.append(result)

        return {
            "success": True,
            "trigger": trigger.code,
            "results": results
        }