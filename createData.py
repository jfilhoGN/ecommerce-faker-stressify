import csv
import random
from faker import Faker
from pymongo import MongoClient
import os
import uuid
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/test")
client = MongoClient(MONGO_URL)
db = client.ecommerce

db_products = db.products
db_users = db.users
db_orders = db.orders

fake = Faker()

output_file = "products.csv"
num_products = 100

def generate_product():
    # Combine duas palavras para gerar um nome de produto mais único
    name = f"{fake.word().capitalize()} {fake.word().capitalize()}"
    description = fake.sentence(nb_words=12)
    price = round(random.uniform(1.0, 500.0), 2)
    stock = random.randint(0, 1000)
    sku = random.randint(100000, 999999)
    return {
        "name": name,
        "description": description,
        "price": price,
        "stock": stock,
        "sku": sku
    }

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "description", "price", "stock", "sku"])
    writer.writeheader()

    for _ in range(num_products):
        product = generate_product()
        writer.writerow(product)

print(f"Arquivo {output_file} gerado com sucesso com {num_products} produtos!")

def initialize_data():
    print('entrou', db_products.count_documents({}))
    if db_products.count_documents({}) == 1:
            try:
                print("Tentando ler o arquivo products.csv...")
                with open("products.csv", mode="r") as csv_file:
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
                
generate_product()
initialize_data()        
