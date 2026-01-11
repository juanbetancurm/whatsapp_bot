from django.db import models
from django.utils import timezone


class Message(models.Model):
    """
    Stores all messages (incoming from users and outgoing from bot)
    """
    
    # Message direction choices
    DIRECTION_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]
    
    # Fields
    phone_number = models.CharField(
        max_length=50,
        help_text="User's phone number in E.164 format (e.g., +573001234567)"
    )
    
    message_text = models.TextField(
        help_text="Content of the message"
    )
    
    direction = models.CharField(
        max_length=10,
        choices=DIRECTION_CHOICES,
        default='incoming',
        help_text="Whether message is from user (incoming) or bot (outgoing)"
    )
    
    timestamp = models.DateTimeField(
        default=timezone.now,
        help_text="When the message was created"
    )
    
    twilio_sid = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Twilio message SID for tracking"
    )
    
    processing_time = models.FloatField(
        null=True,
        blank=True,
        help_text="Time in seconds for Ollama to process (for outgoing messages)"
    )
    
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text="Error details if message failed"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-timestamp']  # Newest first
        indexes = [
            models.Index(fields=['phone_number', '-timestamp']),
            models.Index(fields=['direction', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.direction.upper()} - {self.phone_number} - {self.message_text[:50]}"
    
    def get_short_message(self):
        """Return first 100 characters of message"""
        if len(self.message_text) > 100:
            return f"{self.message_text[:100]}..."
        return self.message_text