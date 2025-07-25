from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import Product, Contact

router = APIRouter()


# Response models
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


class ContactResponse(BaseModel):
    id: int
    telegram_username: Optional[str]  # Raw username for compatibility
    telegram_url: Optional[str]  # Full URL for web apps
    phone_numbers: List[str]  # Raw format for click-to-call
    instagram_username: Optional[str]  # Raw username for compatibility
    instagram_url: Optional[str]  # Full URL for web apps
    is_active: bool

    class Config:
        from_attributes = True


# Health check
@router.get("/health")
async def health_check():
    return {"status": "ok", "app": "Dunya Jewellery API"}


# Products
@router.get("/products", response_model=List[ProductResponse])
async def get_products(active_only: bool = True, db: Session = Depends(get_db)):
    """Get products from database"""
    # Load real products from database
    if active_only:
        products = db.query(Product).filter(Product.is_active == True).all()
    else:
        products = db.query(Product).all()

    # Format response with real data
    result = []
    for product in products:
        result.append(ProductResponse(
            id=product.id,
            title=product.title,
            description=product.description,
            sizes=product.get_sizes_list(),  # Real sizes from database
            telegram_file_ids=product.get_file_ids_list(),  # Real file IDs
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        ))

    return result


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get single product by ID"""
    # Load real product from database
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Return real product data
    return ProductResponse(
        id=product.id,
        title=product.title,
        description=product.description,
        sizes=product.get_sizes_list(),  # Real sizes
        telegram_file_ids=product.get_file_ids_list(),  # Real file IDs
        is_active=product.is_active,
        created_at=product.created_at,
        updated_at=product.updated_at
    )


# Contact (single record)
@router.get("/contact", response_model=ContactResponse)
async def get_contact(db: Session = Depends(get_db)):
    """Get the contact information"""
    # Load real contact from database
    contact = db.query(Contact).first()  # Get the first (and only) contact
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Format URLs for web applications
    telegram_url = None
    if contact.telegram_username:
        telegram_url = f"https://t.me/{contact.telegram_username}"

    instagram_url = None
    if contact.instagram_username:
        instagram_url = f"https://instagram.com/{contact.instagram_username}"

    # Return real contact data with both raw usernames and web URLs
    return ContactResponse(
        id=contact.id,
        telegram_username=contact.telegram_username,  # Raw username
        telegram_url=telegram_url,  # Web URL
        phone_numbers=contact.get_phone_numbers_list(),  # Real phone numbers
        instagram_username=contact.instagram_username,  # Raw username
        instagram_url=instagram_url,  # Web URL
        is_active=contact.is_active
    )


# Product statistics (bonus endpoint)
@router.get("/products/stats")
async def get_product_stats(db: Session = Depends(get_db)):
    """Get product statistics"""
    total_products = db.query(Product).count()
    active_products = db.query(Product).filter(Product.is_active == True).count()
    inactive_products = total_products - active_products

    # Get products with images
    products_with_images = db.query(Product).filter(Product.telegram_file_ids.isnot(None)).filter(
        Product.telegram_file_ids != "").count()

    return {
        "total_products": total_products,
        "active_products": active_products,
        "inactive_products": inactive_products,
        "products_with_images": products_with_images,
        "products_without_images": total_products - products_with_images
    }