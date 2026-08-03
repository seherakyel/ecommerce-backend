from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
import auth
import models
import schemas


# --- Product ---

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 100, search: str = None, category_id: int = None):
    query = db.query(models.Product)
    if search:
        query = query.filter(models.Product.name.ilike(f"{search}%"))
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product


# --- Cart ---

def _get_cart_item(db: Session, item_id: int):
    return (
        db.query(models.CartItem)
        .options(joinedload(models.CartItem.product))
        .filter(models.CartItem.id == item_id)
        .first()
    )


def add_to_cart(db: Session, user_id: int, item: schemas.CartItemCreate):
    product = get_product(db, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    existing = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.user_id == user_id,
            models.CartItem.product_id == item.product_id,
        )
        .first()
    )

    if existing:
        existing.quantity += item.quantity
        db.commit()
        return _get_cart_item(db, existing.id)

    cart_item = models.CartItem(
        user_id=user_id,
        product_id=item.product_id,
        quantity=item.quantity,
    )
    db.add(cart_item)
    db.commit()
    return _get_cart_item(db, cart_item.id)


def get_cart(db: Session, user_id: int):
    return (
        db.query(models.CartItem)
        .options(joinedload(models.CartItem.product))
        .filter(models.CartItem.user_id == user_id)
        .all()
    )


def remove_cart_item(db: Session, item_id: int, user_id: int):
    item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.id == item_id,
            models.CartItem.user_id == user_id,
        )
        .first()
    )
    if item:
        db.delete(item)
        db.commit()
    return item


def clear_cart(db: Session, user_id: int):
    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()


def update_cart_item_quantity(db: Session, item_id: int, user_id: int, quantity: int):
    item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.id == item_id,
            models.CartItem.user_id == user_id,
        )
        .first()
    )
    if not item:
        return None

    if quantity <= 0:
        db.delete(item)
        db.commit()
        return None

    item.quantity = quantity
    db.commit()
    return _get_cart_item(db, item.id)

# --- Order ---

def create_order_from_cart(db: Session, user_id: int):
    cart_items = get_cart(db, user_id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Sepet boş")

    total = 0.0
    order_items_data = []

    for item in cart_items:
        product = item.product
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Yetersiz stok: {product.name} (stok: {product.stock})",
            )
        line_total = product.price * item.quantity
        total += line_total
        order_items_data.append(
            {
                "product_id": product.id,
                "product_name": product.name,
                "quantity": item.quantity,
                "price": product.price,
            }
        )

    db_order = models.Order(user_id=user_id, total=total)
    db.add(db_order)
    db.flush()

    for item_data in order_items_data:
        db.add(models.OrderItem(order_id=db_order.id, **item_data))
        product = get_product(db, item_data["product_id"])
        product.stock -= item_data["quantity"]

    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()

    return get_order(db, db_order.id)


def get_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
        .filter(models.Order.user_id == user_id)
        .order_by(models.Order.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_order(db: Session, order_id: int):
    return (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
        .filter(models.Order.id == order_id)
        .first()
    )


# --- User ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı")

    hashed = auth.hash_password(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    return user


def add_favorite(db: Session, user_id: int, product_id: int):
    existing = (
        db.query(models.Favorite)
        .filter(
            models.Favorite.user_id == user_id,
            models.Favorite.product_id == product_id,
        )
        .first()
    )
    if existing:
        return existing

    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    favorite = models.Favorite(user_id=user_id, product_id=product_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


def get_favorites(db: Session, user_id: int):
    return (
        db.query(models.Favorite)
        .options(joinedload(models.Favorite.product))
        .filter(models.Favorite.user_id == user_id)
        .all()
    )


def remove_favorite(db: Session, user_id: int, product_id: int):
    favorite = (
        db.query(models.Favorite)
        .filter(
            models.Favorite.user_id == user_id,
            models.Favorite.product_id == product_id,
        )
        .first()
    )
    if favorite:
        db.delete(favorite)
        db.commit()
    return favorite


def create_order_from_cart(db: Session, user_id: int, address_id: int):
    cart_items = get_cart(db, user_id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Sepet boş")

    address = (
        db.query(models.Address)
        .filter(
            models.Address.id == address_id,
            models.Address.user_id == user_id,
        )
        .first()
    )
    if not address:
        raise HTTPException(status_code=404, detail="Adres bulunamadı")

    total = 0.0
    order_items_data = []

    for item in cart_items:
        product = item.product
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Yetersiz stok: {product.name} (stok: {product.stock})",
            )
        line_total = product.price * item.quantity
        total += line_total
        order_items_data.append(
            {
                "product_id": product.id,
                "product_name": product.name,
                "quantity": item.quantity,
                "price": product.price,
            }
        )

    db_order = models.Order(user_id=user_id, address_id=address_id, total=total)
    db.add(db_order)
    db.flush()

    for item_data in order_items_data:
        db.add(models.OrderItem(order_id=db_order.id, **item_data))
        product = get_product(db, item_data["product_id"])
        product.stock -= item_data["quantity"]

    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()

    return get_order(db, db_order.id)


def get_addresses(db: Session, user_id: int):
    return db.query(models.Address).filter(models.Address.user_id == user_id).all()


def delete_address(db: Session, address_id: int, user_id: int):
    address = (
        db.query(models.Address)
        .filter(
            models.Address.id == address_id,
            models.Address.user_id == user_id,
        )
        .first()
    )
    if address:
        db.delete(address)
        db.commit()
    return address



def update_address(db: Session, address_id: int, user_id: int, address: schemas.AddressCreate):
    db_address = (
        db.query(models.Address)
        .filter(
            models.Address.id == address_id,
            models.Address.user_id == user_id,
        )
        .first()
    )
    if not db_address:
        return None

    for key, value in address.model_dump().items():
        setattr(db_address, key, value)

    db.commit()
    db.refresh(db_address)
    return db_address


def create_address(db: Session, user_id: int, address: schemas.AddressCreate):
    db_address = models.Address(user_id=user_id, **address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, parent_id=category.parent_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session, parent_id: int = None):
    query = db.query(models.Category)
    if parent_id is None:
        query = query.filter(models.Category.parent_id.is_(None))
    else:
        query = query.filter(models.Category.parent_id == parent_id)
    return query.all()