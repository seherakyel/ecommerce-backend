from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/cart", tags=["sepet"])


@router.post("/items", response_model=schemas.CartItemResponse)
def sepete_ekle(item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    return crud.add_to_cart(db, item)


@router.get("/{session_id}", response_model=list[schemas.CartItemResponse])
def sepeti_goster(session_id: str, db: Session = Depends(get_db)):
    return crud.get_cart(db, session_id)


@router.delete("/items/{item_id}")
def sepetten_sil(item_id: int, session_id: str, db: Session = Depends(get_db)):
    item = crud.remove_cart_item(db, item_id, session_id)
    if not item:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı")
    return {"mesaj": "Ürün sepetten silindi"}
