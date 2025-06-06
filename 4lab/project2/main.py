from fastapi import FastAPI, HTTPException
from typing import List, Optional
from models import StoreAdd, StoreResponse, ProductAdd, ProductResponse
import sqlite3

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в API для управления магазинами и товарами!"}

#Функции для базы данных
def get_db_connection():
    connection = sqlite3.connect("store.db")
    connection.row_factory = sqlite3.Row
    return connection

def get_store(store_id: int):
    connection = get_db_connection()
    store = connection.execute("SELECT * FROM stores WHERE id = ?", (store_id,)).fetchone()
    connection.close()
    return store

def get_product(product_id: int):
    connection = get_db_connection()
    product = connection.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    connection.close()
    return product

#Маршруты для магазинов
@app.get("/stores", response_model=List[StoreResponse])
def get_stores():
    connection = get_db_connection()
    stores = connection.execute("SELECT * FROM stores").fetchall()
    connection.close()
    return [dict(store) for store in stores]

@app.post("/stores", response_model=StoreResponse, status_code=201)
def create_store(store: StoreAdd):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO stores (name, address) VALUES (?, ?)", (store.name, store.address))
    store_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return {"id": store_id, "name": store.name, "address": store.address}

@app.get("/stores/{store_id}/products", response_model=List[ProductResponse])
def get_store_products(store_id: int):
    if not get_store(store_id):
        raise HTTPException(status_code=404, detail="Магазин не найден")
    connection = get_db_connection()
    products = connection.execute("SELECT * FROM products WHERE store_id = ?", (store_id,)).fetchall()
    connection.close()
    return [dict(product) for product in products]

@app.put("/stores/{store_id}", response_model=StoreResponse)
def update_store(store_id: int, store: StoreAdd):
    if not get_store(store_id):
        raise HTTPException(status_code=404, detail="Магазин не найден")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE stores SET name = ?, address = ? WHERE id = ?", (store.name, store.address, store_id))
    connection.commit()
    connection.close()
    return {"id": store_id, "name": store.name, "address": store.address}

#Маршруты для товаров
@app.get("/products", response_model=List[ProductResponse])
def get_products(store_id: Optional[int] = None):
    connection = get_db_connection()
    query = "SELECT * FROM products"
    params = []
    if store_id is not None:
        query += " WHERE store_id = ?"
        params.append(store_id)
    products = connection.execute(query, params).fetchall()
    connection.close()
    return [dict(product) for product in products]

@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductAdd):
    if not get_store(product.store_id):
        raise HTTPException(status_code=404, detail="Магазин не найден")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, store_id) VALUES (?, ?, ?)",
        (product.name, product.price, product.store_id)
    )
    product_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return {"id": product_id, "name": product.name, "price": product.price, "store_id": product.store_id}

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    if not get_product(product_id):
        raise HTTPException(status_code=404, detail="Товар не найден")
    connection = get_db_connection()
    connection.execute("DELETE FROM products WHERE id = ?", (product_id,))
    connection.commit()
    connection.close()
    return {"detail": "Товар удалён"}