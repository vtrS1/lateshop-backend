import uuid
from typing import List

from app.models.user import User
from app.schemas.user import CreateUser
from app.services.auth import hash_password
from sqlalchemy.orm import Session


def get_by_id(db: Session, user_id: uuid) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def create(db: Session, user: CreateUser):
    user_orm = User()
    user_orm.from_pydantic(user)
    db.add(user_orm)
    db.commit()
    db.refresh(user_orm)
    return user_orm


def user_exists(db: Session, user: CreateUser) -> bool:
    by_email = db.query(User).filter(User.email == user.email).first()
    if by_email:
        return True
    return False

