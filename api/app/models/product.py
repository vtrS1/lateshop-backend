import uuid

from app.config.database import Base
from app.schemas.product import CreateProduct
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.category import Category


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String(50), nullable=False)
    price = Column(String(50), nullable=False)
    categories_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    category = relationship(Category, back_populates="products")
    stock = Column(Integer, nullable=False)
    

    def from_pydantic(self, product: CreateProduct):
        self.description = product.description
        self.price = product.price
        self.stock = product.stock
        self.categories_id = product.category_id