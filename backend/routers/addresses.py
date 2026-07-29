from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post("/", response_model=schemas.AddressResponse)
def create_address(
    address: schemas.AddressCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_address(db, current_user.id, address)


@router.get("/", response_model=list[schemas.AddressResponse])
def get_addresses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_addresses(db, current_user.id)


@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    address = crud.delete_address(db, address_id, current_user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Adres bulunamadı")
    return {"message": "Adres silindi"}


@router.patch("/{address_id}", response_model=schemas.AddressResponse)
def update_address(
    address_id: int,
    address: schemas.AddressCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    updated = crud.update_address(db, address_id, current_user.id, address)
    if not updated:
        raise HTTPException(status_code=404, detail="Adres bulunamadı")
    return updated