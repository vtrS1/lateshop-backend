from datetime import datetime, timedelta

from app.config.environment import get_settings
from app.repositories import user as user_repository
from app.schemas.auth import TokenData
from app.schemas.user import ShowUser
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db: Session, email: str, password: str):
    user = user_repository.get_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise Exception("Invalid Credentials")

    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password):
    return pwd_context.hash(plain_password)


def create_access_token(data: dict):
    access_token_expires = timedelta(
        minutes=get_settings().jwt_access_token_expire_minutes
    )
    to_encode = data.copy()
    expire = datetime.utcnow() + access_token_expires

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, get_settings().jwt_secretkey, algorithm=get_settings().jwt_algorithm
    )
    return encoded_jwt


def get_current_user(token: str, db: Session) -> ShowUser:
    try:
        payload = jwt.decode(
            token,
            get_settings().jwt_secretkey,
            algorithms=[get_settings().jwt_algorithm],
        )
        sub: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        token_data = TokenData(
            email=sub, user_id=user_id
        )
        user = user_repository.get_by_id(db, token_data.user_id)
        if user is None:
            return None
        show_user = ShowUser.from_orm(user)
        return show_user
    except JWTError:
        return None


def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.isnumeric() for char in password):
        return False

    if not any(char in "!@#$%^&*()_+" for char in password):
        return False

    return True


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if not credentials.scheme.lower() == "bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authentication scheme."
            )
        if not self.validate_jwt_token(credentials.credentials):
            raise HTTPException(status_code=401, detail="Invalid authentication token.")
        return credentials.credentials

    def validate_jwt_token(self, token: str) -> bool:
        try:
            jwt.decode(
                token,
                get_settings().jwt_secretkey,
                algorithms=[get_settings().jwt_algorithm],
            )
            return True
        except JWTError:
            return False
