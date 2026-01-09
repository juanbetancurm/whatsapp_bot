import requests
import logging
import time

logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Handles communication with local Ollama instance
    """
    
    def __init__(self, model="phi3:mini", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
        
    def is_available(self):
        """
        Check if Ollama is running and responsive
        """
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama not available: {e}")
            return False
    
    def generate_response(self, user_message, max_length=1000):
        """
        Send message to Ollama and get AI response
        
        Args:
            user_message (str): The user's message
            max_length (int): Maximum characters in response
            
        Returns:
            tuple: (response_text, processing_time) or (None, None) if error
        """
        start_time = time.time()
        
        try:
            # Prepare the prompt
            prompt = self._create_prompt(user_message)
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,  # Get complete response at once
                "options": {
                    "temperature": 0.7,  # Creativity level (0-1)
                    "top_p": 0.9,
                    "max_tokens": 500,  # Limit response length
                }
            }
            
            logger.info(f"Sending to Ollama: {user_message[:50]}...")
            
            # Send request to Ollama
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=30  # 30 second timeout
            )
            
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse response
            result = response.json()
            ai_response = result.get('response', '').strip()
            
            # Truncate if too long
            if len(ai_response) > max_length:
                ai_response = ai_response[:max_length] + "..."
            
            processing_time = time.time() - start_time
            
            logger.info(f"Ollama responded in {processing_time:.2f}s")
            
            return ai_response, processing_time
            
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            return None, None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
            return None, None
            
        except Exception as e:
            logger.error(f"Unexpected error with Ollama: {e}")
            return None, None
    
    def _create_prompt(self, user_message):
        """
        Create a well-formatted prompt for the AI
        """
        system_context = """Eres un asistente virtual amigable que ayuda 
        a las personas por WhatsApp. 
        Fuiste integrado por un desarrollador fullstack y profe de matemáticas 
        llamado Juan Betancur  
        Responde de manera concisa, clara y útil. 
        Si no sabes algo, dilo honestamente.
        Responde en el mismo idioma que el usuario."""
        
        prompt = f"""{system_context}

Usuario: {user_message}

Asistente:"""
        
        return prompt
    
    def get_fallback_message(self):
        """
        Return a fallback message when Ollama is unavailable
        """
        return """Lo siento, estoy experimentando problemas técnicos en este momento. 
Por favor, intenta de nuevo en unos minutos. 🤖"""


# Create a singleton instance
ollama_client = OllamaClient()