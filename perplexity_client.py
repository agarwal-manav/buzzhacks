import os
import json
import requests
from typing import Optional, Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerplexityClient:
    """
    A client for interacting with Perplexity AI API.
    Supports chat completions and text generation.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Perplexity client.
        
        Args:
            api_key (str, optional): Your Perplexity API key. If not provided, 
                                   will try to get from PERPLEXITY_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set PERPLEXITY_API_KEY environment variable or pass it to the constructor.")
        
        self.base_url = "https://api.perplexity.ai"
        self.default_model = "sonar-pro"  # Reverted to working model
        
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       model: Optional[str] = None,
                       max_tokens: Optional[int] = None,
                       temperature: Optional[float] = None,
                       top_p: Optional[float] = None) -> Dict[str, Any]:
        """
        Send a chat completion request to Perplexity API.
        
        Args:
            messages (List[Dict]): List of message dictionaries with 'role' and 'content' keys
            model (str, optional): Model to use (default: sonar-pro)
            max_tokens (int, optional): Maximum number of tokens to generate
            temperature (float, optional): Controls randomness (0.0 to 2.0)
            top_p (float, optional): Nucleus sampling parameter
            
        Returns:
            Dict containing the API response
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model or self.default_model,
            "messages": messages
        }
        
        # Add optional parameters if provided
        if max_tokens is not None:
            data["max_tokens"] = max_tokens
        if temperature is not None:
            data["temperature"] = temperature
        if top_p is not None:
            data["top_p"] = top_p
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to Perplexity API: {e}")
            raise
    
    def generate_text(self, 
                     prompt: str, 
                     model: Optional[str] = None,
                     max_tokens: Optional[int] = None,
                     temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Generate text using Perplexity API.
        
        Args:
            prompt (str): The input prompt for text generation
            model (str, optional): Model to use
            max_tokens (int, optional): Maximum number of tokens to generate
            temperature (float, optional): Controls randomness (0.0 to 2.0)
            
        Returns:
            Dict containing the API response
        """
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        return self.chat_completion(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )
    
    def chat(self, 
             messages: List[Dict[str, str]], 
             model: Optional[str] = None,
             max_tokens: Optional[int] = None,
             temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Have a conversation with Perplexity.
        
        Args:
            messages (List[Dict]): List of message dictionaries with 'role' and 'content' keys
            model (str, optional): Model to use
            max_tokens (int, optional): Maximum number of tokens to generate
            temperature (float, optional): Controls randomness (0.0 to 2.0)
            
        Returns:
            Dict containing the API response
        """
        # Filter out system messages and ensure proper format
        filtered_messages = []
        for msg in messages:
            if msg.get('role') in ['user', 'assistant']:
                filtered_messages.append(msg)
        
        return self.chat_completion(
            messages=filtered_messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )
    
    def analyze_content(self, 
                       text: str, 
                       analysis_type: str = "general",
                       model: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze content using Perplexity API.
        
        Args:
            text (str): Text to analyze
            analysis_type (str): Type of analysis (e.g., "sentiment", "summary", "general")
            model (str, optional): Model to use
            
        Returns:
            Dict containing the analysis results
        """
        analysis_prompts = {
            "sentiment": "Analyze the sentiment of the following text and provide a detailed explanation:",
            "summary": "Provide a concise summary of the following text:",
            "general": "Analyze the following text and provide insights about its content, style, and key points:"
        }
        
        prompt = f"{analysis_prompts.get(analysis_type, analysis_prompts['general'])}\n\n{text}"
        return self.generate_text(prompt, model=model)
    
    def extract_text_from_response(self, response: Dict[str, Any]) -> str:
        """
        Extract the generated text from the API response.
        
        Args:
            response (Dict): The API response dictionary
            
        Returns:
            str: The generated text
        """
        try:
            choices = response.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                return message.get("content", "")
            return ""
        except (KeyError, IndexError) as e:
            logger.error(f"Error extracting text from response: {e}")
            return ""

# Example usage and utility functions
def create_perplexity_client(api_key: Optional[str] = None) -> PerplexityClient:
    """
    Create a Perplexity client instance.
    
    Args:
        api_key (str, optional): Your Perplexity API key
        
    Returns:
        PerplexityClient: Configured client instance
    """
    return PerplexityClient(api_key)

def test_perplexity_connection(api_key: str) -> bool:
    """
    Test the connection to Perplexity API.
    
    Args:
        api_key (str): Your Perplexity API key
        
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        client = PerplexityClient(api_key)
        response = client.generate_text("Hello, this is a test message.")
        return "choices" in response
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    print("Perplexity API Client")
    print("=" * 50)
    
    # Your API key
    api_key = "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"
    
    print(f"Using model: sonar-pro")
    
    try:
        # Create client
        client = create_perplexity_client(api_key)
        
        # Test basic text generation
        print("Testing text generation...")
        response = client.generate_text(
            "Write a short poem about artificial intelligence.",
            max_tokens=200,
            temperature=0.8
        )
        
        generated_text = client.extract_text_from_response(response)
        print(f"Generated text:\n{generated_text}")
        
        # Test chat functionality
        print("\nTesting chat functionality...")
        messages = [
            {"role": "user", "content": "What is machine learning?"},
            {"role": "assistant", "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed."},
            {"role": "user", "content": "Can you give me a simple example?"}
        ]
        
        chat_response = client.chat(messages, max_tokens=300)
        chat_text = client.extract_text_from_response(chat_response)
        print(f"Chat response:\n{chat_text}")
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set your PERPLEXITY_API_KEY environment variable or pass it to the constructor.")
    except Exception as e:
        print(f"Error: {e}") 