from fastapi import FastAPI, HTTPException, Query, Body
from typing import List, Optional, Dict, Any
import uvicorn
from models import ShopWithCategories, CategoryWithAttributes, Product, APIResponse, ProductFilter
from data_loader import SHOPS, CATEGORIES, PRODUCTS, get_products_by_category_and_attributes, get_product_by_id

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

# 1. List Shops API
@app.get("/shops", response_model=APIResponse)
async def list_shops():
    """
    List all shops with their details including:
    - Shop metadata (name, description, image_url)
    - List of categories with metadata
    """
    return APIResponse(
        success=True,
        data=list(SHOPS.values())
    )

# 2. List Categories API
@app.get("/categories", response_model=APIResponse)
async def list_categories():
    """
    List all categories with:
    - Category metadata (name, description, image_url)
    - List of attributes for each category
    - List of possible values for each attribute
    """
    return APIResponse(
        success=True,
        data=list(CATEGORIES.values())
    )

# 2b. Get Category by ID API
@app.get("/categories/{category_id}", response_model=APIResponse)
async def get_category_by_id(category_id: str):
    """
    Get a specific category by its ID
    Returns category information including:
    - Category metadata (name, description, image_url)
    - List of attributes for the category
    - List of possible values for each attribute
    """
    if category_id not in CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return APIResponse(
        success=True,
        data=CATEGORIES[category_id]
    )

# 3. Get Products API
@app.post("/products", response_model=APIResponse)
async def get_products(
    category: str = Body(..., description="Category ID to filter products"),
    filters: List[ProductFilter] = Body(default=[], description="List of attribute filters")
):
    """
    Get products by category with optional attribute filters
    Returns:
    - List of product IDs with complete data
    - Product image, name, price, reviews
    - Product metadata and attributes
    """
    if category not in CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Convert filters to the expected format
    filter_dicts = [{"attribute": f.attribute, "value": f.value} for f in filters]
    
    products = get_products_by_category_and_attributes(category, filter_dicts)
    
    return APIResponse(
        success=True,
        data=products,
        message=f"Found {len(products)} products for category '{category}'"
    )

# 4. Get Product by ID API
@app.get("/products/{product_id}", response_model=APIResponse)
async def get_product_by_id_endpoint(product_id: str):
    """
    Get a specific product by its ID
    Returns complete product information including:
    - Product details (name, description, price, image)
    - Reviews and ratings
    - All attributes and metadata
    """
    product = get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return APIResponse(
        success=True,
        data=product
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 