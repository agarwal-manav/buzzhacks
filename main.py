from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models import APIResponse, AgentRequest, AgentResponse, CategoriesRequest, CategoriesResponse, TryProductOnImageRequest, TryProductOnImageResponse
from data_loader import CATEGORIES, SHOPS
import httpx
from service.try_on_service import TryOnService

app = FastAPI(
    title="E-commerce Backend API",
    description="Backend API for e-commerce platform with shops, categories, and products",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

try_on_service = TryOnService()

@app.get("/", response_model=APIResponse)
async def root():
    """Root endpoint with API information"""
    return APIResponse(
        success=True,
        data={
            "message": "E-commerce Backend API",
            "version": "1.0.0",
            "endpoints": {
                "list_shops": "GET /shops - List all shops with categories and metadata",
                "list_categories": "GET /categories - List all categories with attributes and their values",
                "get_category_by_id": "GET /categories/{category_id} - Get specific category by ID",
                "get_products": "POST /products - Get products by category with optional attribute filters",
                "get_product_by_id": "GET /products/{product_id} - Get specific product by ID",
                "agent_wrapper": "POST /agent - Wrapper for n8n agent webhook with prompts and products array"
            }
        }
    )

# 1. List Categories API
"""
Request:
{
    "shop_id": 1,
}
Response
{
    "first_prompt": "",
    "categories": [
        {
            "name": "Sarees",
            "images": [
                "<img_url_1>",
                ...
            ]
        }
    ]
}
"""
@app.post("/categories", response_model=CategoriesResponse)
async def list_categories(request: CategoriesRequest):
    if request.shop_id not in SHOPS:
        raise HTTPException(status_code=404, detail=f"Shop with ID '{request.shop_id}' not found")
    
    categories = [category for category in CATEGORIES.values() if category.shop_id == request.shop_id]
    return CategoriesResponse(
        first_prompt=SHOPS[request.shop_id].first_prompt,
        categories=categories
    )

# 2. Agent Wrapper API to get products from prompt 
@app.post("/products", response_model=AgentResponse)
async def agent_wrapper(request: AgentRequest):
    """
    Wrapper API that forwards requests to the n8n agent webhook to get products from prompt
    Accepts prompts list and products array, returns complete response with AI answer and full products array
    """
    
    n8n_webhook_url = "http://localhost:5678/webhook/eded0c77-3125-45ab-9796-7501a498d3be"
    
    # Map prompts to webhook's expected format with products array
    request_data = {
        "history": [{"role": "user", "content": prompt} for prompt in request.prompts],
        "products": request.products if request.products is not None else []
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                n8n_webhook_url,
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=90.0  # 90 second timeout
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            
            webhook_response = response.json()
            
            # Return the complete response with full products array
            ai_response = webhook_response.get("ai_response", "")
            products = webhook_response.get("products", [])
            
            return AgentResponse(
                ai_response=ai_response,
                products=products
            )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to agent timed out")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to connect to agent: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Agent returned error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 3. Try product on user image
"""
Request:
{
    "product_img_url": "",
    "user_img_url": ""
}
Respose:
{
    "img_url": ""
}
"""
@app.post("/try_product_on_image", response_model=TryProductOnImageResponse)
async def try_product_on_image(request: TryProductOnImageRequest):
    return TryProductOnImageResponse(img_url=try_on_service.try_on(request.product_img_url, request.user_img_url))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
