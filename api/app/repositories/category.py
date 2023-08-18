from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CreateCategory
from uuid import UUID
def get_all(db: Session):
    return db.query(Category).all()

def create(db: Session, category: CreateCategory):
    category_orm = Category()

    category_orm.from_pydantic(category)

    db.add(category_orm)
    db.commit()
    db.refresh(category_orm)

    return category_orm

def delete(db: Session, id: UUID):
    db.query(Category).filter(Category.id == id).delete()
    db.commit()