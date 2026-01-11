from twilio.rest import Client
from twilio.request_validator import RequestValidator
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)


class TwilioClient:
    """
    Handles communication with Twilio API
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Load from environment variables
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER_ID')
        
        # Validate credentials
        if not self.account_sid:
            logger.warning("TWILIO_ACCOUNT_SID not found in environment")
        if not self.auth_token:
            logger.warning("TWILIO_AUTH_TOKEN not found in environment")
        if not self.whatsapp_number:
            logger.warning("TWILIO_WHATSAPP_NUMBER_ID not found in environment")
        
        # Only create client if we have credentials
        if all([self.account_sid, self.auth_token, self.whatsapp_number]):
            self.client = Client(self.account_sid, self.auth_token)
            self.validator = RequestValidator(self.auth_token)
            logger.info("Twilio client initialized successfully")
        else:
            self.client = None
            self.validator = None
            logger.error("Twilio client could not be initialized - missing credentials")
        
        self._initialized = True
    
    def is_configured(self):
        """Check if Twilio is properly configured"""
        return all([self.account_sid, self.auth_token, self.whatsapp_number, self.client])
    
    def send_message(self, to_number, message_text):
        """
        Send WhatsApp message to user
        
        Args:
            to_number (str): Recipient phone number (e.g., 'whatsapp:+573001234567')
            message_text (str): Message to send
            
        Returns:
            str: Message SID if successful, None if failed
        """
        if not self.is_configured():
            logger.error("Cannot send message - Twilio not configured")
            return None
            
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            logger.info(f"Sending message to {to_number}")
            
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                body=message_text,
                to=to_number
            )
            
            logger.info(f"Message sent successfully. SID: {message.sid}")
            return message.sid
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return None
    
    def validate_request(self, url, post_data, signature):
        """
        Validate that request actually came from Twilio
        
        Args:
            url (str): Full URL of your webhook
            post_data (dict): POST data from request
            signature (str): X-Twilio-Signature header
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not self.validator:
            logger.warning("Cannot validate request - Twilio not configured")
            return True  # Allow through if not configured (for development)
        
        return self.validator.validate(url, post_data, signature)


# Create a function to get the client
def get_twilio_client():
    """Get or create the Twilio client instance"""
    return TwilioClient()