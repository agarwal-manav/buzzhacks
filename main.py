from fastapi import FastAPI, HTTPException
from typing import List
import uvicorn
from models import APIResponse, CategoriesRequest
from data_loader import CATEGORIES, SHOPS

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
                "get_product_by_id": "GET /products/{product_id} - Get specific product by ID"
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
@app.post("/categories", response_model=APIResponse)
async def list_categories(request: CategoriesRequest):
    if request.shop_id not in SHOPS:
        raise HTTPException(status_code=404, detail=f"Shop with ID '{request.shop_id}' not found")
    
    categories = [category for category in CATEGORIES.values() if category.shop_id == request.shop_id]
    return APIResponse(
        success=True,
        data={
            "first_prompt": SHOPS[request.shop_id].first_prompt,
            "categories": categories
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
