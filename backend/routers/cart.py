from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/items", response_model=schemas.CartItemResponse)
def add_to_cart(
    item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.add_to_cart(db, current_user.id, item)


@router.get("/", response_model=list[schemas.CartItemResponse])
def show_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_cart(db, current_user.id)


@router.delete("/items/{item_id}")
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = crud.remove_cart_item(db, item_id, current_user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı")
    return {"mesaj": "Ürün sepetten silindi"}


@router.patch("/items/{item_id}", response_model=schemas.CartItemResponse)
def update_count(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = crud.update_cart_item_quantity(db, item_id, current_user.id, quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı veya silindi")
    return item