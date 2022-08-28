from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"]
)
redis = get_redis_connection(
    host = "redis-11390.c99.us-east-1-4.ec2.cloud.redislabs.com",
    port = "11390",
    password = "VkmxykEWz564iQZhd6v2BEKzPWXe6WQC",
    # decode_response = True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get("/products")
def all():
    return [format(_) for _ in Product.all_pks()]

@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)

def format(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }

@app.post("/products")
def create(product: Product):
    return product.save()

@app.delete("/products/{pk}")
def remove(pk: str):
    Product.delete(pk)