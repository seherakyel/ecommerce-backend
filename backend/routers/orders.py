from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/orders", tags=["siparişler"])


@router.post("/", response_model=schemas.OrderResponse)
def siparis_olustur(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order_from_cart(db, order)


@router.get("/", response_model=list[schemas.OrderResponse])
def siparisleri_listele(db: Session = Depends(get_db)):
    return crud.get_orders(db)


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def siparis_getir(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    return order
