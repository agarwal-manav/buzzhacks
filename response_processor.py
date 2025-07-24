import re
from typing import Dict, Any, Optional

class ResponseProcessor:
    """
    Middle layer for processing Perplexity API responses.
    Extracts different parts of the response for display in different sections.
    """
    
    @staticmethod
    def process_shopkeeper_response(response_text: str) -> Dict[str, Any]:
        """
        Process the shopkeeper response and extract different parts.
        
        Args:
            response_text (str): Raw response from Perplexity API
            
        Returns:
            Dict containing:
            - chat_message: Text to display in chat window (only the dialogue part)
            - selected_category: Extracted category
            - confidence: Extracted confidence percentage
            - confidence_value: Numeric confidence value
            - full_response: Complete response for debugging
            - has_recommendation: Boolean indicating if recommendation is complete
        """
        result = {
            'chat_message': '',
            'selected_category': 'Not determined yet',
            'confidence': '0%',
            'confidence_value': 0,
            'full_response': response_text,
            'has_recommendation': False
        }
        
        # Check if this is a final recommendation response
        if 'Selected Category' in response_text and 'Confidence' in response_text:
            result['has_recommendation'] = True
            
            # Extract the text dialogue part (before the numbered sections)
            # Look for the pattern: numbered sections starting with "1. Text Dialogue"
            sections = re.split(r'\d+\.\s+', response_text)
            
            if len(sections) >= 2:
                # The first section (before "1.") is the chat message
                result['chat_message'] = sections[0].strip()
                
                # Extract category and confidence from the numbered sections
                for section in sections[1:]:
                    if 'Selected Category' in section:
                        category_match = re.search(r'Selected Category[:\s]*([^\n]+)', section, re.IGNORECASE)
                        if category_match:
                            result['selected_category'] = category_match.group(1).strip()
                    
                    if 'Confidence' in section:
                        confidence_match = re.search(r'Confidence[:\s]*(\d+)%', section, re.IGNORECASE)
                        if confidence_match:
                            result['confidence'] = confidence_match.group(1) + '%'
                            result['confidence_value'] = int(confidence_match.group(1))
            else:
                # Fallback: if no numbered sections, try to extract from the whole text
                result['chat_message'] = response_text
                
                category_match = re.search(r'Selected Category[:\s]*([^\n]+)', response_text, re.IGNORECASE)
                if category_match:
                    result['selected_category'] = category_match.group(1).strip()
                
                confidence_match = re.search(r'Confidence[:\s]*(\d+)%', response_text, re.IGNORECASE)
                if confidence_match:
                    result['confidence'] = confidence_match.group(1) + '%'
                    result['confidence_value'] = int(confidence_match.group(1))
        else:
            # This is a regular chat message, not a final recommendation
            result['chat_message'] = response_text
        
        return result
    
    @staticmethod
    def extract_chat_message_only(response_text: str) -> str:
        """
        Extract only the chat message part for display in the chat window.
        
        Args:
            response_text (str): Raw response from Perplexity API
            
        Returns:
            str: Only the chat message part
        """
        # If it's a final recommendation, extract the dialogue part
        if 'Selected Category' in response_text and 'Confidence' in response_text:
            # Split by numbered sections and take the first part
            sections = re.split(r'\d+\.\s+', response_text)
            if len(sections) >= 2:
                return sections[0].strip()
        
        # If it's a regular message, return the whole text
        return response_text
    
    @staticmethod
    def is_final_recommendation(response_text: str) -> bool:
        """
        Check if the response contains a final recommendation.
        
        Args:
            response_text (str): Raw response from Perplexity API
            
        Returns:
            bool: True if it's a final recommendation
        """
        return 'Selected Category' in response_text and 'Confidence' in response_text
    
    @staticmethod
    def get_confidence_level(confidence_value: int) -> str:
        """
        Get confidence level description.
        
        Args:
            confidence_value (int): Numeric confidence value
            
        Returns:
            str: Confidence level description
        """
        if confidence_value >= 75:
            return 'high'
        elif confidence_value >= 50:
            return 'medium'
        else:
            return 'low'

# Example usage
if __name__ == "__main__":
    # Test the processor
    processor = ResponseProcessor()
    
    # Test case 1: Regular chat message
    test_response1 = "That's great! I can see you're looking for something comfortable and casual. For everyday wear, I'd recommend checking out our T-shirts. They come in various styles and materials. What's your preferred fit - loose, regular, or fitted?"
    
    result1 = processor.process_shopkeeper_response(test_response1)
    print("Test 1 - Regular Chat Message:")
    print(f"Chat Message: {result1['chat_message']}")
    print(f"Has Recommendation: {result1['has_recommendation']}")
    print()
    
    # Test case 2: Final recommendation
    test_response2 = """Based on our conversation, I can see you're looking for comfortable, casual everyday wear with a preference for loose-fitting items and cotton material.

1. Text Dialogue:
Customer: I need something casual for everyday wear
Shopkeeper: That's great! I can see you're looking for something comfortable and casual. For everyday wear, I'd recommend checking out our T-shirts. They come in various styles and materials. What's your preferred fit - loose, regular, or fitted?
Customer: I prefer loose fit and cotton material
Shopkeeper: Perfect! Our loose-fit cotton T-shirts would be ideal for you. They're comfortable, breathable, and perfect for everyday wear.

2. Selected Category: Tshirt

3. Confidence: 85%"""
    
    result2 = processor.process_shopkeeper_response(test_response2)
    print("Test 2 - Final Recommendation:")
    print(f"Chat Message: {result2['chat_message']}")
    print(f"Selected Category: {result2['selected_category']}")
    print(f"Confidence: {result2['confidence']}")
    print(f"Has Recommendation: {result2['has_recommendation']}")
    print(f"Confidence Level: {processor.get_confidence_level(result2['confidence_value'])}") 