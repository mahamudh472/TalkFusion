from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests
import logging
from rest_framework import status
import json

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


class WhatsAppWebhookView(APIView):
    def get(self, request):
        """
        Handle webhook verification (GET request from Meta).
        """
        mode = request.query_params.get('hub.mode')
        token = request.query_params.get('hub.verify_token')
        challenge = request.query_params.get('hub.challenge')

        if mode == 'subscribe' and token == settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN:
            logger.info('Webhook verification successful')
            return Response(challenge, content_type='text/plain')
        else:
            logger.warning(f'Webhook verification failed: mode={mode}, token={token}')
            return Response({'error': 'Invalid verification token'}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        """
        Handle incoming webhook events (POST request from Meta).
        """
        try:
            payload = request.data
            logger.info(f'Received webhook payload: {json.dumps(payload, indent=2)}')

            if payload.get('object') == 'whatsapp_business_account':
                for entry in payload.get('entry', []):
                    for change in entry.get('changes', []):
                        if change.get('field') == 'messages':
                            value = change['value']
                            messages = value.get('messages', [])
                            statuses = value.get('statuses', [])

                            # Handle incoming messages
                            for message in messages:
                                sender = message.get('from')
                                message_type = message.get('type')
                                message_content = message.get(message_type, {}).get('body', 'Non-text message')
                                logger.info(f'Incoming message from {sender}: {message_content}')
                                # Add logic: e.g., save to DB, trigger reply via API

                            # Handle message status updates (e.g., sent, delivered, read)
                            for status_update in statuses:
                                message_id = status_update.get('id')
                                status_type = status_update.get('status')
                                recipient = status_update.get('recipient_id')
                                logger.info(f'Message {message_id} to {recipient} status: {status_type}')
                                # Add logic: e.g., update message status in DB

            return Response({'status': 'Event received'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error processing webhook: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)