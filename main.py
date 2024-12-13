from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

import sqlite3

app = FastAPI()


class Customer(BaseModel):
    name: str
    phone: str


class Item(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    customer_id: int
    item_name: str
    notes: str
    timestamp: int


def get_db_connection():
    conn = sqlite3.connect('db.sqlite', timeout=30, check_same_thread=False)  
    conn.row_factory = sqlite3.Row
    return conn



@app.post("/customers")
def create_customer(customer: Customer, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()  
        raise HTTPException(status_code=400, detail="Customer with this name and phone already exists")
    except sqlite3.OperationalError as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()  

    return {"message": "Customer created successfully"}


@app.get("/customers/{id}")
def get_customer(id: int, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        customer = cursor.execute("SELECT * FROM customers WHERE id = ?", (id,)).fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return dict(customer)
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()  


@app.get("/all_customers")
def get_all_customers(conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        customers = cursor.execute("SELECT * FROM customers").fetchall()
        if not customers:
            raise HTTPException(status_code=404, detail="No customers found")
        customer_dict = {row["id"]: {"name": row["name"], "phone": row["phone"]} for row in customers}
        return customer_dict
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()  


# Items Endpoints
@app.post("/items")
def create_item(item: Item, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()  
        raise HTTPException(status_code=400, detail="Item already exists")
    except sqlite3.OperationalError as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()  

    return {"message": "Item created successfully"}


@app.get("/items/{name}")
def get_item(name: str, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        item = cursor.execute("SELECT * FROM items WHERE name = ?", (name,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return dict(item)
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()  


# Orders Endpoints
@app.post("/orders")
def create_order(order: Order, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO orders (customer_id, item_name, notes, timestamp) VALUES (?, ?, ?, ?)",
                       (order.customer_id, order.item_name, order.notes, order.timestamp))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()  
        raise HTTPException(status_code=400, detail="Order already exists")
    except sqlite3.OperationalError as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()  

    return {"message": "Order created successfully"}


@app.get("/orders/{id}")
def get_order(id: int, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        order = cursor.execute("SELECT * FROM orders WHERE id = ?", (id,)).fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return dict(order)
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()  
