from app.config.database import get_db
from app.config.jwt import oauth2_scheme
from app.repositories import user as user_repository
from app.schemas.auth import OAuth2LoginRequest, Token
from app.schemas.user import ShowUser
from app.services import auth as auth_service
from app.services.auth import authenticate_user, create_access_token, get_current_user
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["auth"],
    prefix="/auth",
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2LoginRequest,
    db: Session = Depends(get_db),
):
    user_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user = authenticate_user(db, form_data.email, form_data.password)
    except Exception as e:
        user_exception.detail = str(e)
        raise user_exception

    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": str(user.id),
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me", dependencies=[Depends(auth_service.JWTBearer())], response_model=ShowUser
)
async def read_users_me(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user