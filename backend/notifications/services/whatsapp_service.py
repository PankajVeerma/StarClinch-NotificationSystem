import requests

from django.conf import settings


class WhatsAppService:

    @staticmethod
    def send_message(phone_number, message):

        if not phone_number:
            return {
                "success": False,
                "channel": "WHATSAPP",
                "message": "Phone number is required."
            }

        if not message:
            return {
                "success": False,
                "channel": "WHATSAPP",
                "message": "Message is required."
            }

        access_token = settings.WHATSAPP_ACCESS_TOKEN
        phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        api_version = settings.WHATSAPP_API_VERSION
        print("Access Token",access_token)
        print("phone_number_id",phone_number_id)
        url = (
            f"https://graph.facebook.com/"
            f"{api_version}/"
            f"{phone_number_id}/messages"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        
        # Replace your current payload block with this to test connectivity:
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {
                    "code": "en_US"
                }
            }
        }
        # payload = {
        #     "messaging_product": "whatsapp",
        #     "to": phone_number,
        #     "type": "text",
        #     "text": {
        #         "body": message,
        #     }
        # }

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
                    "success": True,
                    "channel": "WHATSAPP",
                    "message": "WhatsApp message sent successfully.",
                    "provider_response": response_data,
                }

            return {
                "success": False,
                "channel": "WHATSAPP",
                "message": "WhatsApp message failed.",
                "provider_response": response_data,
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "channel": "WHATSAPP",
                "message": "WhatsApp API request timed out."
            }

        except requests.exceptions.RequestException as e:

            return {
                "success": False,
                "channel": "WHATSAPP",
                "message": f"WhatsApp API request failed: {str(e)}"
            }

        except Exception as e:
            print("Exception Error", e)
            return {
                "success": False,
                "channel": "WHATSAPP",
                "message": f"Unexpected error: {str(e)}"
            }