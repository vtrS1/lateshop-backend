from app.config.database import get_db
from app.repositories import user as user_repository
from app.schemas.user import (
    CreateUser,
    ShowUser
)
from app.services import auth as auth_service
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["users"],
    prefix="/users",
)

@router.post(
    "/",
    response_model=ShowUser,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: CreateUser,
    db: Session = Depends(get_db),
):
    user_exists = user_repository.user_exists(db, user)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User Already registered"
        )

    if not auth_service.validate_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Password Format",
        )
    user.password = auth_service.hash_password(user.password)
    db_user = user_repository.create(db, user)
    return ShowUser.from_orm(db_user)

