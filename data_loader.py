import json
import os
from typing import List, Dict, Any
from models import ShopWithCategories, CategoryMetadata

def load_json_file(filename: str, folder: str = "static") -> Any:
    """Load JSON data from a file in the specified directory"""
    file_path = os.path.join(folder, filename)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_normalized_data():
    """Load all normalized data and reconstruct the full objects"""
    
    # Load base data files
    category_metadata = load_json_file("category_metadata.json")
    shops_data = load_json_file("shops.json")

    # Reconstruct category objects with full attribute information
    categories = {}
    for category_id, metadata in category_metadata.items():        
        # Create full category object
        categories[category_id] = CategoryMetadata(
            id=metadata["id"],
            name=metadata["name"],
            images=metadata["images"],
            shop_id=metadata["shop_id"]
        )

    # Reconstruct shop objects with full category information
    shops = {}
    for shop_id, shop_info in shops_data.items():
        # Get full category objects for this shop
        shop_categories = []
        for category in categories.values():
            if category.shop_id == shop_id:
                shop_categories.append(category)
        
        # Create full shop object
        shops[shop_id] = ShopWithCategories(
            id=shop_info["id"],
            name=shop_info["name"],
            first_prompt=shop_info["first_prompt"],
            categories=shop_categories
        )

    return shops, categories

# Load all normalized data
SHOPS, CATEGORIES = load_normalized_data()
