from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .ollama_utils import ollama_client
from .models import Message
from .twilio_utils import get_twilio_client
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


@csrf_exempt  # For testing only
@require_http_methods(["GET"])
def test_chat(request):
    """
    Test endpoint to verify Ollama integration without WhatsApp
    Usage: http://localhost:8000/test-chat/?message=Hola
    """
    
    # Get message from URL parameter
    user_message = request.GET.get('message', '')
    
    if not user_message:
        return JsonResponse({
            'error': 'Please provide a message parameter',
            'example': '/test-chat/?message=Hola'
        }, status=400)
    
    # Check if Ollama is available
    if not ollama_client.is_available():
        return JsonResponse({
            'error': 'Ollama is not running',
            'solution': 'Start Ollama: ollama serve'
        }, status=503)
    
    # Save incoming message to database
    incoming_msg = Message.objects.create(
        phone_number='test_user',
        message_text=user_message,
        direction='incoming'
    )
    
    logger.info(f"Test message received: {user_message}")
    
    # Get AI response
    ai_response, processing_time = ollama_client.generate_response(user_message)
    
    if ai_response is None:
        # Ollama failed
        error_msg = ollama_client.get_fallback_message()
        
        outgoing_msg = Message.objects.create(
            phone_number='test_user',
            message_text=error_msg,
            direction='outgoing',
            error_message='Ollama unavailable'
        )
        
        return JsonResponse({
            'status': 'error',
            'user_message': user_message,
            'bot_response': error_msg,
            'error': 'Ollama unavailable'
        }, status=500)
    
    # Save outgoing message to database
    outgoing_msg = Message.objects.create(
        phone_number='test_user',
        message_text=ai_response,
        direction='outgoing',
        processing_time=processing_time
    )
    
    logger.info(f"Test response sent: {ai_response[:50]}...")
    
    return JsonResponse({
        'status': 'success',
        'user_message': user_message,
        'bot_response': ai_response,
        'processing_time': f"{processing_time:.2f}s",
        'incoming_message_id': incoming_msg.id,
        'outgoing_message_id': outgoing_msg.id
    })


@require_http_methods(["GET"])
def health_check(request):
    """
    Check if all systems are operational
    Usage: http://localhost:8000/health/
    """
    
    # Check Ollama
    ollama_status = ollama_client.is_available()
    
    # Check database
    try:
        Message.objects.count()
        db_status = True
    except Exception as e:
        logger.error(f"Database error: {e}")
        db_status = False
    
    return JsonResponse({
        'status': 'healthy' if (ollama_status and db_status) else 'unhealthy',
        'ollama': 'running' if ollama_status else 'not available',
        'database': 'connected' if db_status else 'error',
        'model': ollama_client.model
    })

@csrf_exempt
@require_http_methods(["POST"])
def whatsapp_webhook(request):
    """
    Webhook endpoint that receives messages from Twilio WhatsApp
    
    Twilio sends POST request here when user sends WhatsApp message
    """
    
    logger.info("=" * 50)
    logger.info("WEBHOOK RECEIVED")
    logger.info("=" * 50)
    
    try:
        # Extract data from Twilio's request
        from_number = request.POST.get('From', '')  # Format: whatsapp:+573001234567
        to_number = request.POST.get('To', '')      # Your bot number
        message_body = request.POST.get('Body', '')
        message_sid = request.POST.get('MessageSid', '')
        
        logger.info(f"From: {from_number}")
        logger.info(f"Message: {message_body}")
        logger.info(f"SID: {message_sid}")
        
        # Validate required fields
        if not all([from_number, message_body]):
            logger.error("Missing required fields")
            return HttpResponse(status=400)
        
        # Save incoming message to database
        incoming_message = Message.objects.create(
            phone_number=from_number,
            message_text=message_body,
            direction='incoming',
            twilio_sid=message_sid
        )
        
        logger.info(f"Saved incoming message ID: {incoming_message.id}")
        
        # Check if Ollama is available
        if not ollama_client.is_available():
            logger.error("Ollama is not available")
            error_response = ollama_client.get_fallback_message()
            
            # Save error response
            Message.objects.create(
                phone_number=from_number,
                message_text=error_response,
                direction='outgoing',
                error_message='Ollama unavailable'
            )
            
            # Send error message to user
            get_twilio_client().send_message(from_number, error_response)
            
            return HttpResponse(status=200)  # Always return 200 to Twilio
        
        # Generate AI response
        ai_response, processing_time = ollama_client.generate_response(message_body)
        
        if ai_response is None:
            logger.error("Ollama failed to generate response")
            ai_response = ollama_client.get_fallback_message()
            processing_time = 0
        
        logger.info(f"AI Response: {ai_response[:100]}...")
        logger.info(f"Processing time: {processing_time:.2f}s")
        
        # Send response back to user via WhatsApp
        response_sid = get_twilio_client().send_message(from_number, ai_response)
        
        # Save outgoing message to database
        outgoing_message = Message.objects.create(
            phone_number=from_number,
            message_text=ai_response,
            direction='outgoing',
            twilio_sid=response_sid,
            processing_time=processing_time
        )
        
        logger.info(f"Saved outgoing message ID: {outgoing_message.id}")
        logger.info("=" * 50)
        logger.info("WEBHOOK COMPLETED SUCCESSFULLY")
        logger.info("=" * 50)
        
        # IMPORTANT: Always return 200 to Twilio
        return HttpResponse(status=200)
        
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        # Still return 200 to prevent Twilio retries
        return HttpResponse(status=200)