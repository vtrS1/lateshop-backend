from typing import List
from uuid import UUID

from app.config.environment import get_settings
from app.repositories import user as user_repository
from app.schemas.user import (
    CreateUser,
    ShowUser,
    UpdateNameAndEmail,
    UpdatePasswordData,
)
from app.services import auth as auth_service
from pydantic import parse_obj_as
from sqlalchemy.orm import Session


def get_users(db: Session) -> List[ShowUser]:
    users = user_repository.get_users(db)

    users = [user for user in users if not user.deleted]

    return parse_obj_as(List[ShowUser], users)


def get_user(db: Session, user_id: UUID) -> ShowUser:
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise Exception("User not found")

    return ShowUser.from_orm(user)


def change_password(db: Session, token: str, password: str):
    if not auth_service.validate_password(password):
        raise Exception("Invalid password format")

    user = user_repository.get_by_token(db, token)
    if not user:
        raise Exception("Invalid Token")

    user = user_repository.change_password(db, user, password)

    user_repository.change_user_token(db, user)

    return user


def get_username_by_token(token: str, db: Session) -> str:
    if not token:
        raise Exception("Token string can not be empty")

    user = user_repository.get_by_token(db, token)

    if not user:
        raise Exception("User not found for the specified token")

    return user.name


def update_user(db: Session, user_id: UUID, user: CreateUser):
    updated_user = user_repository.update_user(db, user_id, user)

    if not updated_user:
        raise Exception("Unable to update user")

    return updated_user


def toogle_deactivate_user(db: Session, user_id: UUID):
    user = user_repository.deactivate_user(db, user_id)
    if not user:
        raise Exception("Unable to deactivate user")

    return user


def get_user_by_email(db: Session, email: str) -> ShowUser:
    user = user_repository.get_by_email(db, email)
    if not user:
        raise Exception("User not found")

    return ShowUser.from_orm(user)


def delete_user(db: Session, user_id: UUID):
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise Exception("User not found")
    if user.is_active:
        raise Exception("You can not delete an active user")

    user_repository.delete_user(db, user_id)
    if not user:
        raise Exception("Unable to delete user")

    return user


def update_password(db: Session, user_id: UUID, data: UpdatePasswordData):
    if not auth_service.validate_password(data.new_password):
        raise Exception("Invalid password format")

    if data.new_password != data.confirm_password:
        raise Exception("Passwords do not match")

    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise Exception("User not found")

    if not auth_service.verify_password(data.old_password, user.password):
        raise Exception("Invalid password")

    user_repository.change_password(db, user, data.new_password)

    return user


def simple_update_user(db: Session, user_id: UUID, user: UpdateNameAndEmail):
    updated_user = user_repository.simple_update_user(db, user_id, user)
    if not updated_user:
        raise Exception("Unable to update user")

    return updated_user
