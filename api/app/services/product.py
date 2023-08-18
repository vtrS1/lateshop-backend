from typing import List
from uuid import UUID
from app.repositories import product as product_respository
from app.schemas.product import ShowProduct, CreateProduct
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

def get_all(db: Session):
    categories = product_respository.get_all(db)
    return parse_obj_as(List[ShowProduct], categories)

def create(db: Session, category: CreateProduct):
    category = product_respository.create(db, category)
    return ShowProduct.from_orm(category)


def delete(db: Session, id: UUID):
    product_respository.delete(db, id)