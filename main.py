from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime

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
    item_id: int
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


@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
    except sqlite3.OperationalError as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

    return {"message": "Customer updated successfully"}


@app.delete("/customers/{id}")
def delete_customer(id: int, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
    except sqlite3.OperationalError as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

    return {"message": "Customer deleted successfully"}


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


@app.get("/items/{id}")
def get_item(id: int, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        item = cursor.execute("SELECT * FROM items WHERE id = ?", (id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return dict(item)
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.put("/items/{id}")
def update_item(id: int, item: Item, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
    except sqlite3.OperationalError as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

    return {"message": "Item updated successfully"}


@app.delete("/items/{id}")
def delete_item(id: int, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM items WHERE id = ?", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
    except sqlite3.OperationalError as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

    return {"message": "Item deleted successfully"}


@app.post("/orders")
def create_order(order: Order, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    if order.timestamp is None or order.timestamp == 0:
        order.timestamp = int(datetime.utcnow().timestamp())
    try:
        cursor.execute("INSERT INTO orders (customer_id, item_id, notes, timestamp) VALUES (?, ?, ?, ?)",
                       (order.customer_id, order.item_id, order.notes, order.timestamp))
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


@app.put("/orders/{id}")
def update_order(id: int, order: Order, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    if order.timestamp is None or order.timestamp == 0:
        order.timestamp = int(datetime.utcnow().timestamp())
    try:
        cursor.execute("UPDATE orders SET customer_id = ?, item_id = ?, notes = ?, timestamp = ? WHERE id = ?",
                       (order.customer_id, order.item_id, order.notes, order.timestamp, id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
    except sqlite3.OperationalError as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

    return {"message": "Order updated successfully"}


@app.delete("/orders/{id}")
def delete_order(id: int, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
    except sqlite3.OperationalError as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

    return {"message": "Order deleted successfully"}
