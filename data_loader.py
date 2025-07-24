import json
import os
from typing import List, Dict, Any
from models import ShopWithCategories, CategoryWithAttributes, Product, ProductReview

def load_json_file(filename: str) -> Any:
    """Load JSON data from a file in the static directory"""
    file_path = os.path.join("static", filename)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_shops() -> Dict[str, ShopWithCategories]:
    """Load shops data from JSON and convert to Pydantic models"""
    shops_data = load_json_file("shops.json")
    shops = {}
    
    for shop_id, shop_info in shops_data.items():
        shops[shop_id] = ShopWithCategories(**shop_info)
    
    return shops

def load_categories() -> Dict[str, CategoryWithAttributes]:
    """Load categories data from JSON and convert to Pydantic models"""
    categories_data = load_json_file("categories.json")
    categories = {}
    
    for category_id, category_info in categories_data.items():
        categories[category_id] = CategoryWithAttributes(**category_info)
    
    return categories

def load_products() -> List[Product]:
    """Load products data from JSON and convert to Pydantic models"""
    products_data = load_json_file("products.json")
    products = []
    
    for product_info in products_data:
        # Convert reviews dict to ProductReview model
        if "reviews" in product_info:
            product_info["reviews"] = ProductReview(**product_info["reviews"])
        
        products.append(Product(**product_info))
    
    return products

# Load all data at module level (cached)
SHOPS = load_shops()
CATEGORIES = load_categories() 
PRODUCTS = load_products()

def get_products_by_category_and_attributes(category_id: str, attribute_filters: list = None):
    """Get products filtered by category and optional attribute filters"""
    if attribute_filters is None:
        attribute_filters = []
    
    # Convert list of filters to dict for easier processing
    filters_dict = {}
    for filter_item in attribute_filters:
        if isinstance(filter_item, dict) and "attribute" in filter_item and "value" in filter_item:
            filters_dict[filter_item["attribute"]] = filter_item["value"]
    
    filtered_products = []
    for product in PRODUCTS:
        if product.category_id != category_id:
            continue
            
        # Check if product matches all attribute filters
        match = True
        for attr_id, attr_value in filters_dict.items():
            if attr_id not in product.attributes or product.attributes[attr_id] != attr_value:
                match = False
                break
                
        if match:
            filtered_products.append(product)
    
    return filtered_products

def get_product_by_id(product_id: str):
    """Get a specific product by ID"""
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    return None 