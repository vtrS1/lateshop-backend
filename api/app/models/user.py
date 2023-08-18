import uuid

from app.config.database import Base
from app.schemas.user import CreateUser
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    def from_pydantic(self, user: CreateUser):
        self.name = user.name
        self.email = user.email
        self.password = user.password