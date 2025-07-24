#!/usr/bin/env python3
"""
Test script for Gemini API using the provided API key.
"""

from gemini_client import GeminiClient, test_gemini_connection

# Your API key
API_KEY = "AIzaSyDOwduspBj_fs5NXvE51jxfvSvpuvUmUfE"

def test_connection():
    """Test the connection to Gemini API."""
    print("Testing Gemini API connection...")
    print("=" * 50)
    
    success = test_gemini_connection(API_KEY)
    if success:
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")
    return success

def test_text_generation():
    """Test text generation functionality."""
    print("\nTesting text generation...")
    print("=" * 50)
    
    try:
        client = GeminiClient(API_KEY)
        
        # Test 1: Simple text generation
        print("1. Simple text generation:")
        response = client.generate_text(
            "Write a haiku about programming",
            max_tokens=100,
            temperature=0.7
        )
        text = client.extract_text_from_response(response)
        print(f"Response: {text}")
        
        # Test 2: Creative writing
        print("\n2. Creative writing:")
        response = client.generate_text(
            "Create a short story about a robot learning to paint",
            max_tokens=300,
            temperature=0.9
        )
        text = client.extract_text_from_response(response)
        print(f"Response: {text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Text generation failed: {e}")
        return False

def test_chat_functionality():
    """Test chat conversation functionality."""
    print("\nTesting chat functionality...")
    print("=" * 50)
    
    try:
        client = GeminiClient(API_KEY)
        
        messages = [
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "model", "content": "The capital of France is Paris."},
            {"role": "user", "content": "What are some famous landmarks there?"}
        ]
        
        response = client.chat(messages, max_tokens=200, temperature=0.7)
        text = client.extract_text_from_response(response)
        print(f"Chat response: {text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chat functionality failed: {e}")
        return False

def test_content_analysis():
    """Test content analysis functionality."""
    print("\nTesting content analysis...")
    print("=" * 50)
    
    try:
        client = GeminiClient(API_KEY)
        
        sample_text = """
        Artificial Intelligence is transforming the world around us. 
        From virtual assistants to autonomous vehicles, AI technologies 
        are becoming increasingly integrated into our daily lives. 
        While this brings many benefits, it also raises important 
        questions about privacy, job displacement, and ethical considerations.
        """
        
        # Test sentiment analysis
        print("1. Sentiment analysis:")
        response = client.analyze_content(sample_text, "sentiment")
        text = client.extract_text_from_response(response)
        print(f"Sentiment: {text}")
        
        # Test summary
        print("\n2. Summary:")
        response = client.analyze_content(sample_text, "summary")
        text = client.extract_text_from_response(response)
        print(f"Summary: {text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Content analysis failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Gemini API Test Suite")
    print("=" * 50)
    
    # Test connection
    if not test_connection():
        print("❌ Cannot proceed without connection. Please check your API key.")
        return
    
    # Test text generation
    test_text_generation()
    
    # Test chat functionality
    test_chat_functionality()
    
    # Test content analysis
    test_content_analysis()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\nYou can now use the GeminiClient in your project:")
    print("from gemini_client import GeminiClient")
    print("client = GeminiClient('your-api-key')")

if __name__ == "__main__":
    main() 