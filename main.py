from fastapi import FastAPI, HTTPException
from typing import List
import uvicorn
from models import APIResponse, AgentRequest, AgentResponse, CategoriesRequest, CategoriesResponse, ProductResponse
from data_loader import CATEGORIES, SHOPS
import httpx
from pydantic import BaseModel

app = FastAPI(
    title="E-commerce Backend API",
    description="Backend API for e-commerce platform with shops, categories, and products",
    version="1.0.0"
)

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
                "agent_wrapper": "POST /products - Wrapper for n8n agent webhook with prompts list"
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
            "category_name": "Sarees",
            "category_images": [
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
    Accepts prompts list and returns simplified response with AI answer and products
    """
    import random
    
    n8n_webhook_url = "http://localhost:5678/webhook/eded0c77-3125-45ab-9796-7501a498d3be"
    
    # Map prompts to webhook's expected history format
    request_data = {
        "history": [{"role": "user", "content": prompt} for prompt in request.prompts],
        "preferences": {}
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
            
            # Transform response to match the required format
            ai_response = webhook_response.get("ai_response", "")
            
            # Transform products to simplified format
            products = []
            if "products" in webhook_response and webhook_response["products"]:
                for product in webhook_response["products"]:
                    # Generate mock price and rating since not in original data
                    mock_price = round(random.uniform(150.0, 500.0), 2)
                    mock_rating = round(random.uniform(3.5, 5.0), 1)
                    
                    # Get the first image URL if available
                    image_url = ""
                    if product.get("images") and len(product["images"]) > 0:
                        image_url = product["images"][0]
                    
                    # Transform taxonomy attributes to "field_name::value" format
                    taxonomy_attrs = []
                    if product.get("taxonomy_attributes"):
                        for attr in product["taxonomy_attributes"]:
                            field_name = attr.get("field_name", "")
                            value = attr.get("value", "")
                            if field_name and value:
                                taxonomy_attrs.append(f"{field_name}::{value}")
                    
                    products.append(ProductResponse(
                        product_id=product.get("id", 0),
                        product_name=product.get("name", ""),
                        price=mock_price,
                        rating=mock_rating,
                        image_url=image_url,
                        taxonomy_attributes=taxonomy_attrs
                    ))
            
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
