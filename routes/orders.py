from fastapi import APIRouter, HTTPException
from models.models import Order, CartItem
from database.database import db_orders, db_products, db_users
import uuid

router = APIRouter()

@router.post("/orders", response_model=Order)
def create_order(user_id: str, items: list[CartItem]):
    user = db_users.find_one({"id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total = 0
    for item in items:
        product = db_products.find_one({"id": item.product_id}, {"_id": 0})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        if product['stock'] < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product['name']}")
        total += product['price'] * item.quantity
        db_products.update_one({"id": item.product_id}, {"$inc": {"stock": -item.quantity}})

    order = Order(id=str(uuid.uuid4()), user_id=user_id, items=items, total=total)
    db_orders.insert_one(order.dict())
    return order

@router.get("/orders", response_model=list[Order])
def get_orders():
    orders = list(db_orders.find({}, {"_id": 0}))
    return orders

@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    order = db_orders.find_one({"id": order_id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order