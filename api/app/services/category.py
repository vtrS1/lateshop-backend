from typing import List
from uuid import UUID
from app.repositories import category as category_respository
from app.schemas.category import ShowCategory, CreateCategory
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

def get_all(db: Session):
    categories = category_respository.get_all(db)
    return parse_obj_as(List[ShowCategory], categories)

def create(db: Session, category: CreateCategory):
    category = category_respository.create(db, category)
    return ShowCategory.from_orm(category)


def delete(db: Session, id: UUID):
    category_respository.delete(db, id)