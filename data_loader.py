import json
import os
from typing import List, Dict, Any
from models import ShopWithCategories, CategoryWithAttributes, Product, ProductReview, CategoryMetadata, AttributeWithValues

def load_json_file(filename: str, folder: str = "static") -> Any:
    """Load JSON data from a file in the specified directory"""
    file_path = os.path.join(folder, filename)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_normalized_data():
    """Load all normalized data and reconstruct the full objects"""
    
    # Load base data files
    attributes_data = load_json_file("attributes.json")
    category_metadata = load_json_file("category_metadata.json")
    category_attributes_mapping = load_json_file("category_attributes.json")
    shops_data = load_json_file("shops.json")
    products_data = load_json_file("products.json")
    
    # Reconstruct attribute objects
    attributes = {}
    for attr_id, attr_info in attributes_data.items():
        attributes[attr_id] = AttributeWithValues(**attr_info)
    
    # Reconstruct category objects with full attribute information
    categories = {}
    for category_id, metadata in category_metadata.items():
        # Get attribute IDs for this category
        attribute_ids = category_attributes_mapping.get(category_id, [])
        
        # Build full attribute objects
        category_attributes = []
        for attr_id in attribute_ids:
            if attr_id in attributes:
                category_attributes.append(attributes[attr_id])
        
        # Create full category object
        categories[category_id] = CategoryWithAttributes(
            id=metadata["id"],
            name=metadata["name"],
            description=metadata["description"],
            image_url=metadata["image_url"],
            attributes=category_attributes
        )
    
    # Reconstruct shop objects with full category information
    shops = {}
    for shop_id, shop_info in shops_data.items():
        # Get full category objects for this shop
        shop_categories = []
        for category_id in shop_info.get("category_ids", []):
            if category_id in category_metadata:
                shop_categories.append(CategoryMetadata(**category_metadata[category_id]))
        
        # Create full shop object
        shops[shop_id] = ShopWithCategories(
            id=shop_info["id"],
            name=shop_info["name"],
            description=shop_info["description"],
            image_url=shop_info["image_url"],
            categories=shop_categories
        )
    
    # Reconstruct product objects (already well normalized)
    products = []
    for product_info in products_data:
        # Convert reviews dict to ProductReview model
        if "reviews" in product_info:
            product_info["reviews"] = ProductReview(**product_info["reviews"])
        
        products.append(Product(**product_info))
    
    return shops, categories, products, attributes

# Load all normalized data
SHOPS, CATEGORIES, PRODUCTS, ATTRIBUTES = load_normalized_data()

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

# Additional utility functions for normalized data
def get_attribute_by_id(attribute_id: str):
    """Get a specific attribute definition by ID"""
    return ATTRIBUTES.get(attribute_id)

def get_attributes_for_category(category_id: str) -> List[AttributeWithValues]:
    """Get all attribute definitions for a specific category"""
    if category_id in CATEGORIES:
        return CATEGORIES[category_id].attributes
    return [] 