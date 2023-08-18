from pydantic import BaseModel, UUID4

class CategoryBase(BaseModel):
    description: str

    class Config:
        orm_mode = True

class ShowCategory(CategoryBase):
    id:UUID4

class CreateCategory(CategoryBase):
    pass