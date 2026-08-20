from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request
from dependencies import get_current_user
from redis_client import check_rate_limit
from database import get_db
import models,crud,schemas,auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host
    check_rate_limit(f"ratelimit:login:{client_ip}", limit=5, window=60)
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="E-posta veya şifre hatalı")
    token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=schemas.UserResponse)
def update_me(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.update_user(db, current_user.id, user_update)