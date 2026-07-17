from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

import models
import schemas


# --- Ürün ---

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product


# --- Sepet ---

def _get_cart_item(db: Session, item_id: int):
    return (
        db.query(models.CartItem)
        .options(joinedload(models.CartItem.product))
        .filter(models.CartItem.id == item_id)
        .first()
    )


def add_to_cart(db: Session, item: schemas.CartItemCreate):
    product = get_product(db, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    existing = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.session_id == item.session_id,
            models.CartItem.product_id == item.product_id,
        )
        .first()
    )

    if existing:
        existing.quantity += item.quantity
        db.commit()
        return _get_cart_item(db, existing.id)

    cart_item = models.CartItem(**item.model_dump())
    db.add(cart_item)
    db.commit()
    return _get_cart_item(db, cart_item.id)


def get_cart(db: Session, session_id: str):
    return (
        db.query(models.CartItem)
        .options(joinedload(models.CartItem.product))
        .filter(models.CartItem.session_id == session_id)
        .all()
    )


def remove_cart_item(db: Session, item_id: int, session_id: str):
    item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.id == item_id,
            models.CartItem.session_id == session_id,
        )
        .first()
    )
    if item:
        db.delete(item)
        db.commit()
    return item


def clear_cart(db: Session, session_id: str):
    db.query(models.CartItem).filter(models.CartItem.session_id == session_id).delete()
    db.commit()


# --- Sipariş ---

def create_order_from_cart(db: Session, order: schemas.OrderCreate):
    cart_items = get_cart(db, order.session_id)
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

    db_order = models.Order(session_id=order.session_id, total=total)
    db.add(db_order)
    db.flush()

    for item_data in order_items_data:
        db.add(models.OrderItem(order_id=db_order.id, **item_data))
        product = get_product(db, item_data["product_id"])
        product.stock -= item_data["quantity"]

    db.query(models.CartItem).filter(
        models.CartItem.session_id == order.session_id
    ).delete()
    db.commit()

    return get_order(db, db_order.id)


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
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
