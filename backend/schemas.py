from datetime import datetime
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str | None
    last_name: str | None
    phone: str | None

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CategoryCreate(BaseModel):
    name: str
    parent_id: int | None = None
    image_url: str | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    image_url: str | None = None

    model_config = {"from_attributes": True}
    
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    image_url: str | None = None
    category_id: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    image_url: str | None

    model_config = {"from_attributes": True}
    category: CategoryResponse | None = None


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
    address_id: int

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



