from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

import crud
import schemas
import json
from redis_client import redis_client

router = APIRouter(prefix="/products", tags=["products"])

def invalidate_product_cache():
    count = 0
    for key in redis_client.scan_iter("products:*"):
        redis_client.delete(key)
        count += 1


@router.post("/", response_model=schemas.ProductResponse)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = crud.create_product(db, product)
    invalidate_product_cache()
    return new_product


@router.get("/", response_model=list[schemas.ProductResponse])
def list_products(search: str = None, db: Session = Depends(get_db)):
    cache_key = f"products:search:{search}" if search else "products:all"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    products = crud.get_products(db, search=search)
    data = [schemas.ProductResponse.model_validate(p).model_dump() for p in products]
    redis_client.setex(cache_key, 300, json.dumps(data, default=str))
    return data


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


@router.get("/", response_model=list[schemas.ProductResponse])
def list_products(search: str = None, category_id: int = None, db: Session = Depends(get_db)):
    return crud.get_products(db, search=search, category_id=category_id)