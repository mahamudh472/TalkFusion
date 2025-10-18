import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

VERIFY_TOKEN = "my_whatsapp_webhook_token_123"  # Change this!

@csrf_exempt
def webhook(request):
    if request.method == "GET":
        # ✅ Verification request from Meta
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse("Verification token mismatch", status=403)

    elif request.method == "POST":
        # ✅ Incoming message
        data = json.loads(request.body.decode("utf-8"))
        print("Incoming message:", json.dumps(data, indent=2))

        # Example: Extract and log message
        try:
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            messages = value.get("messages")
            if messages:
                phone_number = messages[0]["from"]
                text = messages[0]["text"]["body"]
                print(f"Received message from {phone_number}: {text}")
        except Exception as e:
            print("Error parsing message:", e)

        return HttpResponse("EVENT_RECEIVED")
    else:
        return HttpResponse(status=405)

@csrf_exempt
def fb_webhook(request):
    if request.method == 'GET':
        # Verification
        token_sent = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        if token_sent == "my_fb_webhook_token_123":
            return HttpResponse(challenge)
        return HttpResponse("Invalid verification token", status=403)
    
    elif request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        # Process messages here
        print(data)
        return HttpResponse("EVENT_RECEIVED")
    else:
        return HttpResponse(status=405)
