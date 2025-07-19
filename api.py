from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import Product

router = APIRouter()


# Pydantic schemas (only for responses now)
class ProductResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    sizes: List[float]
    telegram_file_ids: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Read-only endpoints
@router.get("/health")
async def health_check():
    return {"status": "healthy", "app": "Dunya Jewellery API"}


@router.get("/products", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """Get all active products (read-only)"""
    products = db.query(Product).filter(Product.is_active == True).all()

    # Convert to response format
    result = []
    for product in products:
        result.append(ProductResponse(
            id=product.id,
            title=product.title,
            description=product.description,
            sizes=product.get_sizes_list(),
            telegram_file_ids=product.get_file_ids_list(),
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        ))

    return result


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get single product by ID (read-only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return ProductResponse(
        id=product.id,
        title=product.title,
        description=product.description,
        sizes=product.get_sizes_list(),
        telegram_file_ids=product.get_file_ids_list(),
        is_active=product.is_active,
        created_at=product.created_at,
        updated_at=product.updated_at
    )