from pydantic import BaseModel
from typing import List, Any, Optional

class CategoryMetadata(BaseModel):
    id: int
    name: str
    images: List[str]
    shop_id: str

class ShopWithCategories(BaseModel):
    id: str
    name: str
    first_prompt: str
    categories: List[CategoryMetadata]

class CategoriesRequest(BaseModel):
    shop_id: str

class APIResponse(BaseModel):
    success: bool
    data: Any
    message: Optional[str] = None

# Models for the agent wrapper API
class ChatMessage(BaseModel):
    role: str
    content: str

class AgentRequest(BaseModel):
    prompts: List[str]
    products: Optional[List[dict]] = []
class SimpleProduct(BaseModel):
    product_id: int
    product_name: str
    price: float
    rating: float
    image_url: str
    category: str

class AgentResponse(BaseModel):
    ai_response: str
    products: List[SimpleProduct]

class CategoriesResponse(BaseModel):
    first_prompt: str
    categories: List[CategoryMetadata]

class TryProductOnImageRequest(BaseModel):
    product_img_url: str
    user_img_url: str

class TryProductOnImageResponse(BaseModel):
    img_url: str
