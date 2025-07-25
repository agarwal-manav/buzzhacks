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
