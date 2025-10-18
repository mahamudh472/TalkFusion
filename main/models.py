from django.db import models
import uuid

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'companies'


class APIIntegration(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('web_chat', 'Web Chat'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_integrations'
        indexes = [
            # name shortened to <= 30 chars to satisfy some DB backends (Oracle/MySQL) limits
            models.Index(fields=['company'], name='idx_api_integrations_company'),
        ]


class AccessToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api_integration = models.ForeignKey(APIIntegration, on_delete=models.CASCADE)
    token = models.TextField()
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'access_tokens'


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    api_integration = models.ForeignKey(APIIntegration, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversations'


class Message(models.Model):
    SENDER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('ai', 'AI'),
        ('human', 'Human'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    api_integration = models.ForeignKey(APIIntegration, on_delete=models.SET_NULL, null=True, blank=True)
    sender_type = models.CharField(max_length=20, choices=SENDER_TYPE_CHOICES)
    sender_id = models.UUIDField(null=True, blank=True)
    recipient_id = models.UUIDField(null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    is_escalated = models.BooleanField(default=False)

    class Meta:
        db_table = 'messages'
        indexes = [
            models.Index(fields=['conversation'], name='idx_messages_conversation_id'),
        ]


class AIConfiguration(models.Model):
    TONE_CHOICES = [
        ('professional', 'Professional'),
        ('friendly', 'Friendly'),
        ('formal', 'Formal'),
        ('casual', 'Casual'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    tone = models.CharField(max_length=20, choices=TONE_CHOICES, default='professional')
    personality = models.JSONField(null=True, blank=True)
    training_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ai_configurations'