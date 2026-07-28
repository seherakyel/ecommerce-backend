from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("/", response_model=schemas.FavoriteResponse)
def add_favorite(
    favorite: schemas.FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.add_favorite(db, current_user.id, favorite.product_id)


@router.get("/", response_model=list[schemas.FavoriteResponse])
def get_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_favorites(db, current_user.id)


@router.delete("/{product_id}")
def remove_favorite(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    favorite = crud.remove_favorite(db, current_user.id, product_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Favori bulunamadı")
    return {"message": "Ürün favorilerden çıkarıldı"}