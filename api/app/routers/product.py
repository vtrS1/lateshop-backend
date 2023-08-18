
from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.services import auth as auth_service

from app.config.database import get_db
from app.schemas.product import ShowProduct, CreateProduct
from app.services import product as product_service



router = APIRouter(
    prefix="/products",
    tags=["products"]
)



@router.get("/",
            response_model=List[ShowProduct],
            dependencies=[Depends(auth_service.JWTBearer())],
            status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    try:
        products = product_service.get_all(db)
        return products
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Coudn`t fetch all products")
    
@router.post("/",
            response_model=ShowProduct,
            dependencies=[Depends(auth_service.JWTBearer())],
            status_code=status.HTTP_201_CREATED)
def create_product(product: CreateProduct,db: Session = Depends(get_db)):
    try:
        product = product_service.create(db, product)
        return product
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Coudn`t create product")
    
@router.delete("/",
            dependencies=[Depends(auth_service.JWTBearer())],
            status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: UUID,db: Session = Depends(get_db)):
    try:
        product_service.delete(db, id)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Coudn`t delete product")