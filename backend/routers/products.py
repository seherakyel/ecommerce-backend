from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=schemas.ProductResponse)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.get("/", response_model=list[schemas.ProductResponse])
def list_products(search: str = None, db: Session = Depends(get_db)):
    return crud.get_products(db, search=search)


@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return {"mesaj": "Ürün silindi"}