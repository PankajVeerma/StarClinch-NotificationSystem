import requests
from django.conf import settings


class EmailService:

    @staticmethod
    def send_email(to_email, subject, body):

        if not to_email:
            return {
                "channel": "EMAIL",
                "success": False,
                "message": "Recipient email is required."
            }

        if not subject:
            return {
                "channel": "EMAIL",
                "success": False,
                "message": "Email subject is required."
            }

        if not body:
            return {
                "channel": "EMAIL",
                "success": False,
                "message": "Email body is required."
            }

        url = "https://api.postmarkapp.com/email"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": settings.POSTMARKAPP_TOKEN,
        }

        payload = {
            "From": settings.POSTMARK_FROM_EMAIL,
            "To": to_email,
            "Subject": subject,
            "TextBody": body,
            "MessageStream": "outbound",
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )

            response_data = response.json()

            if response.ok:
                return {
                    "channel": "EMAIL",
                    "success": True,
                    "message": "Email sent successfully.",
                    "provider_response": response_data,
                }

            return {
                "channel": "EMAIL",
                "success": False,
                "message": response_data.get(
                    "Message",
                    "Postmark email sending failed."
                ),
                "provider_response": response_data,
            }

        except requests.exceptions.Timeout:
            return {
                "channel": "EMAIL",
                "success": False,
                "message": "Postmark API request timed out."
            }

        except requests.exceptions.RequestException as e:
            return {
                "channel": "EMAIL",
                "success": False,
                "message": f"Postmark API request failed: {str(e)}"
            }

        except Exception as e:
            return {
                "channel": "EMAIL",
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }