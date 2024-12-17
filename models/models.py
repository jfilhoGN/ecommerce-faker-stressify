from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    stock: int

class User(BaseModel):
    id: str
    name: str
    email: str

class CartItem(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    id: str
    user_id: str
    items: List[CartItem]
    total: float