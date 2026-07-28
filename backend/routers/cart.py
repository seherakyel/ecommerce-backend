from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/items", response_model=schemas.CartItemResponse)
def add_to_cart(item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    return crud.add_to_cart(db, item)


@router.get("/{session_id}", response_model=list[schemas.CartItemResponse])
def show_cart(session_id: str, db: Session = Depends(get_db)):
    return crud.get_cart(db, session_id)


@router.delete("/items/{item_id}")
def remove_from_cart(item_id: int, session_id: str, db: Session = Depends(get_db)):
    item = crud.remove_cart_item(db, item_id, session_id)
    if not item:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı")
    return {"mesaj": "Ürün sepetten silindi"}


@router.patch("/items/{item_id}", response_model=schemas.CartItemResponse)
def update_count(item_id: int, session_id: str, quantity: int, db: Session = Depends(get_db)):
    item = crud.update_cart_item_quantity(db, item_id, session_id, quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı veya silindi")
    return item