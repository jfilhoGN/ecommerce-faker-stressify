from fastapi import APIRouter, HTTPException
from models.models import Product
from database.database import db_products
import uuid

router = APIRouter()

@router.get("/products", response_model=list[Product])
def get_products():
    products = list(db_products.find({}, {"_id": 0}))
    return products

@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    product = db_products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=Product)
async def create_product(product: Product):
    existing_product = db_products.find_one({"id": product.id})
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this ID already exists")

    if not product.id:
        product.id = str(uuid.uuid4())

    product_dict = product.dict()
    
    try:
        result = db_products.insert_one(product_dict)
        if result.inserted_id:
            # Retorna o produto recém-criado
            return product
        else:
            raise HTTPException(status_code=500, detail="Failed to create product")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the product: {str(e)}")
