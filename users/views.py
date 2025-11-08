from rest_framework.views import APIView
from rest_framework.response import Response

class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        response_data = {
            "open_chats": 5,
            "appointments_today": 10,
            "new_appointments": 2,
            "payments_today": 150.00,
            "appointments": [
                {"id": 1, "time": "10:00 AM", "client": "John Doe", "status": "confirmed"},
                {"id": 2, "time": "11:30 AM", "client": "Jane Smith", "status": "pending"},
                {"id": 3, "time": "02:00 PM", "client": "Mike Johnson", "status": "confirmed"},
                {"id": 4, "time": "03:15 PM", "client": "Emily Davis", "status": "canceled"},
                {"id": 5, "time": "04:00 PM", "client": "Chris Brown", "status": "confirmed"},
                {"id": 6, "time": "05:30 PM", "client": "Anna Wilson", "status": "pending"},
                {"id": 7, "time": "06:00 PM", "client": "David Lee", "status": "confirmed"},
                {"id": 8, "time": "07:15 PM", "client": "Sophia Martinez", "status": "confirmed"},
                {"id": 9, "time": "08:00 PM", "client": "James Taylor", "status": "canceled"},
                {"id": 10, "time": "09:30 PM", "client": "Olivia Anderson", "status": "confirmed"},
            ],
            "payments": [
                {"id": 1, "amount": 50.00, "reason": "Consultation", "client": "John Doe", "status": "Paid"},
                {"id": 2, "amount": 75.00, "reason": "Follow-up", "client": "Jane Smith", "status": "Pending"},
                {"id": 3, "amount": 25.00, "reason": "Cancellation", "client": "Mike Johnson", "status": "Paid"},
                {"id": 4, "amount": 100.00, "reason": "Therapy Session", "client": "Emily Davis", "status": "Paid"},
                {"id": 5, "amount": 60.00, "reason": "Consultation", "client": "Chris Brown", "status": "Pending"},
                {"id": 6, "amount": 80.00, "reason": "Follow-up", "client": "Anna Wilson", "status": "Paid"},
            ],
            "channels_status" : [
                {"channel": "Whatsapp", "status": "Active"},
                {"channel": "Facebook", "status": "Inactive"},
                {"channel": "Instagram", "status": "Active"},
            ]

        }
        return Response(response_data)