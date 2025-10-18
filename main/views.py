import token
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests
import logging
from rest_framework import status
import json
from allauth.socialaccount.models import SocialToken

logger = logging.getLogger(__name__)

class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})

class SendWhatsappMessageView(APIView):
    def post(self, request):
        data = request.data
        message = data.get("message", "")
        phone_number = data.get("phone_number", "")
        url = "https://graph.facebook.com/v15.0/836297246233728/messages"
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_API_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            # "template": {
            #     "name": "hello_world",
            #     "language": {
            #         "code": "en_US"
            #     }
            # }
            "text": {
                "body": message,
                # "language": {
                #     "code": "en_US"
                # }
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        if response.status_code == 200:
            return Response({"status": "Message sent successfully"})
        else:
            return Response({"status": "Failed to send message", "error": response.text}, status=500)


def custom_view(request):
    user_token_obj = SocialToken.objects.filter(
        account__user=request.user,
        account__provider='facebook'
    ).first()

    if not user_token_obj:
        return JsonResponse({"error": "User has no linked Facebook account"}, status=400)

    user_token = user_token_obj.token

    # Get pages managed by user
    res = requests.get(
        "https://graph.facebook.com/v19.0/me/accounts",
        params={"access_token": user_token}
    )
    pages = res.json()
    if not pages.get("data"):
        return JsonResponse({"error": "No pages found"}, status=400)

    page = pages["data"][0]
    page_id = page["id"]
    page_access_token = page["access_token"]  # <-- THIS IS IMPORTANT

    # Subscribe page to webhook
    # url = f"https://graph.facebook.com/v19.0/{page_id}/subscribed_apps"
    # params = {
    #     "subscribed_fields": "messages,messaging_postbacks",
    #     "access_token": page_access_token  # <-- use page token
    # }
    # response = requests.post(url, params=params)

    # confirm_response = requests.get(
    #     f"https://graph.facebook.com/v19.0/{page_id}/subscribed_apps",
    #     params={"access_token": page_access_token}
    # )

    PSID = "24939509165711051"
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={page_access_token}"

    payload = {
        "recipient": {"id": PSID},
        "message": {"text": "Hello from TalkFusion!"}
    }

    response = requests.post(url, json=payload)

    return JsonResponse({
        "user_token": user_token,
        "pages": pages,
        "page_id": page_id,
        "page_access_token": page_access_token,
        # "subscribe_response": response.json(),
        "message_response": response.json(),
    })
