from fastapi import APIRouter, HTTPException
from models.models import User
from database.database import db_users
import uuid
router = APIRouter()

@router.get("/users", response_model=list[User])
def get_users():
    users = list(db_users.find({}, {"_id": 0}))
    return users

@router.post("/users", response_model=User)
async def create_user(user: User):
    existing_user = db_users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    if not user.id:
        user.id = str(uuid.uuid4())

    product_dict = user.dict()
    
    try:
        result = db_users.insert_one(product_dict)
        if result.inserted_id:
            return user
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the product: {str(e)}")