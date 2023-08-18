import uuid

from app.config.database import Base
from app.schemas.category import CreateCategory
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String(50), nullable=False)
    products = relationship("Product", back_populates="category")
    
    def from_pydantic(self, category: CreateCategory):
        self.description = category.description