from datetime import datetime
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int

    model_config = {"from_attributes": True}


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductResponse

    model_config = {"from_attributes": True}


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: float

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    pass

class OrderResponse(BaseModel):
    id: int
    total: float
    status: str
    created_at: datetime
    items: list[OrderItemResponse]

    model_config = {"from_attributes": True}


class FavoriteCreate(BaseModel):
    product_id: int


class FavoriteResponse(BaseModel):
    id: int
    product: ProductResponse

    model_config = {"from_attributes": True}

class AddressCreate(BaseModel):
    title: str
    full_name: str
    phone: str
    city: str
    district: str
    full_address: str


class AddressResponse(BaseModel):
    id: int
    title: str
    full_name: str
    phone: str
    city: str
    district: str
    full_address: str

    model_config = {"from_attributes": True}