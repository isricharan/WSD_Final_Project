# WSD_Final_Project

This project initializes the customer order database based on the provided json file similar to examples_orders.json and perform CRUD operations on it using FastAPI.

The database contains 3 tables namely customers, items and orders. Orders table contain references to customers and items through item_id and customers_id.

Id's in all the tables are auto incremented with each row addition and for the orders table if timestamp not provided, current timestamp is taken by default.

To initialize the database

python init_db.py

Above command results in db.sqlite file with the database

To run the API's

uvicorn main:app --reload

Use the http://127.0.0.1:8000/docs link to test the API's