from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=schemas.OrderResponse)
def siparis_olustur(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_order_from_cart(db, current_user.id)


@router.get("/", response_model=list[schemas.OrderResponse])
def siparisleri_listele(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_orders(db, current_user.id)


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def siparis_getir(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_order(db, order_id)