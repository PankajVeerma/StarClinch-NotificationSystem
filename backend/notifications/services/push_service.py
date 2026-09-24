import requests

from django.conf import settings


class PushService:

    @staticmethod
    def send_push(subscription,title,body):
        if not subscription:
            return {
                "success": False,
                "channel": "WEB_PUSH",
                "message": "OneSignal subscription ID is required."
            }

        if not title:
            return {
                "success": False,
                "channel": "WEB_PUSH",
                "message": "Notification title is required."
            }

        if not body:
            return {
                "success": False,
                "channel": "WEB_PUSH",
                "message": "Notification body is required."
            }

        url = "https://api.onesignal.com/notifications"

        headers = {
            "Authorization": f"Key {settings.ONESIGNAL_REST_API_KEY}",
            "Content-Type": "application/json",
        }
        
         # Temporary test payload to check if it fires:
        payload = {
            "app_id": settings.ONESIGNAL_APP_ID,
            "included_segments": ["All Subscribers"],  # Target everyone for testing
            "headings": {"en": title},
            "contents": {"en": body}
        }
        # payload = {
        #     "app_id": settings.ONESIGNAL_APP_ID,

            # "include_subscription_ids": [
            #     subscription
            # ],

        #     "headings": {
        #         "en": title
        #     },

        #     "contents": {
        #         "en": body
        #     }
        # }

        try:
            response = requests.post(url,headers=headers,json=payload,timeout=30)

            response_data = response.json()

            if response.ok:
                return {
                    "success": True,
                    "channel": "WEB_PUSH",
                    "message": "Web push notification sent successfully.",
                    "provider_response": response_data
                }

            return {
                "success": False,
                "channel": "WEB_PUSH",
                "message": "OneSignal notification failed.",
                "provider_response": response_data
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "channel": "WEB_PUSH",
                "message": "OneSignal API request timed out."
            }

        except requests.exceptions.RequestException as e:

            return {
                "success": False,
                "channel": "WEB_PUSH",
                "message": f"OneSignal API request failed: {str(e)}"
            }

        except Exception as e:

            return {
                "success": False,
                "channel": "WEB_PUSH",
                "message": f"Unexpected error: {str(e)}"
            }