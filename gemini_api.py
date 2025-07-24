from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from perplexity_client import PerplexityClient
from response_processor import ResponseProcessor

# Initialize FastAPI app
app = FastAPI(
    title="Gemini API Wrapper",
    description="A FastAPI wrapper for Google's Gemini API",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Your Perplexity API key
PERPLEXITY_API_KEY = "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"  # You can also set this as environment variable PERPLEXITY_API_KEY

# Initialize Perplexity client
try:
    perplexity_client = PerplexityClient(PERPLEXITY_API_KEY)
except Exception as e:
    print(f"Failed to initialize Perplexity client: {e}")
    perplexity_client = None

# Pydantic models for request/response
class TextRequest(BaseModel):
    text: str
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 40

class ChatMessage(BaseModel):
    role: str  # "user" or "model"
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class AnalysisRequest(BaseModel):
    text: str
    analysis_type: Optional[str] = "general"  # "sentiment", "summary", "general"
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.3

class GeminiResponse(BaseModel):
    success: bool
    text: str
    full_response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    """Serve the web interface."""
    return FileResponse("static/index.html")

@app.get("/products")
async def products():
    """Serve the product selection page."""
    return FileResponse("static/products.html")

@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "message": "Gemini API Wrapper",
        "version": "1.0.0",
        "endpoints": {
            "/generate": "Generate text from a prompt",
            "/chat": "Have a conversation with Gemini",
            "/analyze": "Analyze content (sentiment, summary, etc.)",
            "/health": "Check API health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if perplexity_client is None:
        raise HTTPException(status_code=503, detail="Perplexity client not initialized")
    
    try:
        # Test connection with a simple request
        response = perplexity_client.generate_text("Hello", max_tokens=10)
        return {"status": "healthy", "perplexity_connection": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Perplexity API connection failed: {str(e)}")

@app.post("/generate", response_model=GeminiResponse)
async def generate_text(request: TextRequest):
    """
    Generate text using Perplexity API.
    
    Args:
        request: TextRequest containing the prompt and generation parameters
        
    Returns:
        GeminiResponse with generated text
    """
    if perplexity_client is None:
        raise HTTPException(status_code=503, detail="Perplexity client not initialized")
    
    try:
        response = perplexity_client.generate_text(
            prompt=request.text,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        generated_text = perplexity_client.extract_text_from_response(response)
        
        return GeminiResponse(
            success=True,
            text=generated_text,
            full_response=response
        )
        
    except Exception as e:
        return GeminiResponse(
            success=False,
            text="",
            error=str(e)
        )

@app.post("/chat", response_model=GeminiResponse)
async def chat_with_perplexity(request: ChatRequest):
    """
    Have a conversation with Perplexity.
    
    Args:
        request: ChatRequest containing conversation messages and parameters
        
    Returns:
        GeminiResponse with Perplexity's reply
    """
    if perplexity_client is None:
        raise HTTPException(status_code=503, detail="Perplexity client not initialized")
    
    try:
        # Convert Pydantic models to dictionaries and filter system messages
        messages = []
        for msg in request.messages:
            if msg.role in ['user', 'assistant']:
                messages.append({"role": msg.role, "content": msg.content})
        
        response = perplexity_client.chat(
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        raw_text = perplexity_client.extract_text_from_response(response)
        
        # Process the response using the middle layer
        processed_response = ResponseProcessor.process_shopkeeper_response(raw_text)
        
        return GeminiResponse(
            success=True,
            text=processed_response['chat_message'],  # Only the chat message for display
            full_response={
                'raw_response': response,
                'processed_response': processed_response
            }
        )
        
    except Exception as e:
        return GeminiResponse(
            success=False,
            text="",
            error=str(e)
        )

@app.post("/analyze", response_model=GeminiResponse)
async def analyze_content(request: AnalysisRequest):
    """
    Analyze content using Perplexity API.
    
    Args:
        request: AnalysisRequest containing text and analysis parameters
        
    Returns:
        GeminiResponse with analysis results
    """
    if perplexity_client is None:
        raise HTTPException(status_code=503, detail="Perplexity client not initialized")
    
    try:
        response = perplexity_client.analyze_content(
            text=request.text,
            analysis_type=request.analysis_type
        )
        
        analyzed_text = perplexity_client.extract_text_from_response(response)
        
        return GeminiResponse(
            success=True,
            text=analyzed_text,
            full_response=response
        )
        
    except Exception as e:
        return GeminiResponse(
            success=False,
            text="",
            error=str(e)
        )

@app.post("/simple")
async def simple_text_generation(text: str = Form(...)):
    """
    Simple endpoint that takes text as input and returns Perplexity's response.
    This is the most straightforward endpoint for basic text generation.
    
    Args:
        text: The input text/prompt
        
    Returns:
        Dictionary with the generated response
    """
    if perplexity_client is None:
        raise HTTPException(status_code=503, detail="Perplexity client not initialized")
    
    try:
        response = perplexity_client.generate_text(text, max_tokens=1000, temperature=0.7)
        generated_text = perplexity_client.extract_text_from_response(response)
        
        return {
            "input": text,
            "response": generated_text,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Perplexity API Server...")
    print("📝 Available endpoints:")
    print("   - POST /simple - Simple text generation")
    print("   - POST /generate - Advanced text generation with parameters")
    print("   - POST /chat - Chat conversation")
    print("   - POST /analyze - Content analysis")
    print("   - GET /health - Health check")
    print("   - GET / - API information")
    print("\n🌐 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False) 