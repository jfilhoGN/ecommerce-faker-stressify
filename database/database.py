import asyncio
from pymongo import MongoClient
import os
import uuid
import csv

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/test")
client = MongoClient(MONGO_URL)
db = client.ecommerce

db_products = db.products
db_users = db.users
db_orders = db.orders

async def initialize_data():
    if db_products.count_documents({}) == 0:
        try:
            print("Tentando ler o arquivo products.csv...")
            with open("../products.csv", mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                products = []
                for row in csv_reader:
                    print(f"Produto lido: {row}")
                    products.append({
                        "id": str(uuid.uuid4()),
                        "name": row["name"],
                        "description": row["description"],
                        "price": float(row["price"]),
                        "stock": int(row["stock"])
                    })
                print(f"Produtos a serem inseridos: {len(products)}")
                for product in products:
                    db_products.insert_one(product)
                    print(f"Produto inserido: {product['name']}")
        except FileNotFoundError:
            print("products.csv file not found. Default products will be loaded.")
            default_products = [
                {"id": str(uuid.uuid4()), "name": "Laptop", "description": "Gaming Laptop", "price": 1500.00, "stock": 10},
                {"id": str(uuid.uuid4()), "name": "Mouse", "description": "Wireless Mouse", "price": 25.00, "stock": 50},
                {"id": str(uuid.uuid4()), "name": "Keyboard", "description": "Mechanical Keyboard", "price": 100.00, "stock": 20},
            ]
            for product in default_products:
                db_products.insert_one(product)
                print(f"Produto padrão inserido: {product['name']}")
        except Exception as e:
            print(f"Erro ao inicializar dados (produtos): {e}")

    if db_users.count_documents({}) == 0:
        users = [
            {"id": str(uuid.uuid4()), "name": "John Doe", "email": "john.doe@example.com"},
            {"id": str(uuid.uuid4()), "name": "Jane Smith", "email": "jane.smith@example.com"},
        ]
        for user in users:
            db_users.insert_one(user)
            print(f"Usuário inserido: {user['name']}")