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
    label: str
    telegram_username: Optional[str]
    phone_number: Optional[str]
    instagram_username: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


# Health check
@router.get("/health")
async def health_check():
    return {"status": "ok", "app": "Dunya Jewellery API"}


# Products
@router.get("/products", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """Get all active products"""
    products = db.query(Product).filter(Product.is_active == True).all()

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
    """Get single product"""
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


# Contacts
@router.get("/contacts", response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_db)):
    """Get all active contacts"""
    contacts = db.query(Contact).filter(Contact.is_active == True).all()

    result = []
    for contact in contacts:
        result.append(ContactResponse(
            id=contact.id,
            label=contact.label,
            telegram_username=contact.telegram_username,
            phone_number=contact.phone_number,
            instagram_username=contact.instagram_username,
            is_active=contact.is_active
        ))

    return result


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Get single contact"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return ContactResponse(
        id=contact.id,
        label=contact.label,
        telegram_username=contact.telegram_username,
        phone_number=contact.phone_number,
        instagram_username=contact.instagram_username,
        is_active=contact.is_active
    )