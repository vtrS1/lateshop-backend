from pydantic import BaseModel, UUID4
from app.schemas.category import ShowCategory
class ProductBase(BaseModel):
    description: str
    price:str
    stock: int
    class Config:
        orm_mode=True

class CreateProduct(ProductBase):
    category_id: UUID4

class ShowProduct(ProductBase):
    id: UUID4
    category: ShowCategory