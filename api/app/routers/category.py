from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.services import auth as auth_service

from app.config.database import get_db
from app.schemas.category import ShowCategory, CreateCategory
from app.services import category as category_service

router = APIRouter(
    prefix="/category",
    tags=["category"]
)

@router.get("/",
            response_model=List[ShowCategory],
            dependencies=[Depends(auth_service.JWTBearer())],
            status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db)):
    try:
        categories = category_service.get_all(db)
        return categories
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Coudn`t fetch all categories")
    
@router.post("/",
            response_model=ShowCategory,
            dependencies=[Depends(auth_service.JWTBearer())],
            status_code=status.HTTP_201_CREATED)
def create_category(category: CreateCategory,db: Session = Depends(get_db)):
    try:
        categories = category_service.create(db, category)
        return categories
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Coudn`t create category")
    
@router.delete("/",
            dependencies=[Depends(auth_service.JWTBearer())],
            status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: UUID,db: Session = Depends(get_db)):
    try:
        category_service.delete(db, id)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Coudn`t delete category")