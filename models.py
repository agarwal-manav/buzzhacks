from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class CategoryMetadata(BaseModel):
    id: str
    name: str
    description: str
    image_url: str

class ShopWithCategories(BaseModel):
    id: str
    name: str
    description: str
    image_url: str
    categories: List[CategoryMetadata]

class AttributeWithValues(BaseModel):
    id: str
    name: str
    type: str  # "text", "number", "select", "multi-select"
    allowed_values: List[str]

class CategoryWithAttributes(BaseModel):
    id: str
    name: str
    description: str
    image_url: str
    attributes: List[AttributeWithValues]

class ProductReview(BaseModel):
    rating: float
    count: int
    average: float

class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    image_url: str
    category_id: str
    shop_id: str
    reviews: ProductReview
    attributes: Dict[str, Any]
    metadata: Dict[str, Any]

class ProductFilter(BaseModel):
    attribute: str
    value: str

class APIResponse(BaseModel):
    success: bool
    data: Any
    message: Optional[str] = None 