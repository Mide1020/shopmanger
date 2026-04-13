from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductImageCreate(BaseModel):
    image_url: str
    is_primary: bool = False

class ProductImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    image_url: str
    is_primary: bool