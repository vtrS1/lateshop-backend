from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import CreateProduct
from uuid import UUID

def get_all(db: Session):
    return db.query(Product).all()

def create(db: Session, product: CreateProduct):
    product_orm = Product()

    product_orm.from_pydantic(product)

    db.add(product_orm)
    db.commit()
    db.refresh(product_orm)

    return product_orm

def delete(db: Session, id: UUID):
    db.query(Product).filter(Product.id == id).delete()
    db.commit()