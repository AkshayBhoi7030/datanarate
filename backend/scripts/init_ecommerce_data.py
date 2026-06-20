
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.rag.schema_introspection import SchemaIntrospectionService
from app.rag.schema_embedding import SchemaEmbeddingService
from app.db.base import Base
from app.models import *  # Import all models to create tables

# Step 1: Create tables
create_tables_sql = """
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    sku VARCHAR(50) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    payment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
"""

# Step 2: Sample data
categories_data = [
    ("Electronics", "Gadgets and devices"),
    ("Clothing", "Apparel and accessories"),
    ("Books", "Books and literature"),
    ("Home & Garden", "Home improvement and gardening"),
    ("Sports", "Sports equipment and apparel")
]

products_data = [
    (1, "Wireless Headphones", "Noise-cancelling wireless headphones", 149.99, 50, "ELEC-001"),
    (1, "Smartphone", "Latest model smartphone", 699.99, 30, "ELEC-002"),
    (1, "Laptop", "High-performance laptop", 1299.99, 20, "ELEC-003"),
    (2, "T-Shirt", "Cotton t-shirt", 29.99, 200, "CLO-001"),
    (2, "Jeans", "Denim jeans", 79.99, 100, "CLO-002"),
    (3, "Python Programming Book", "Learn Python programming", 39.99, 150, "BOOK-001"),
    (3, "Data Science Book", "Introduction to data science", 49.99, 120, "BOOK-002"),
    (4, "Garden Trowel", "Stainless steel garden trowel", 19.99, 80, "HOME-001"),
    (4, "Plant Pot", "Ceramic plant pot", 24.99, 100, "HOME-002"),
    (5, "Yoga Mat", "Non-slip yoga mat", 34.99, 150, "SPORTS-001"),
    (5, "Running Shoes", "Comfortable running shoes", 89.99, 75, "SPORTS-002")
]

first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Amanda", "William", "Olivia", "James", "Sophia", "Richard", "Isabella", "Joseph", "Ava", "Thomas", "Mia", "Daniel", "Charlotte"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
countries = ["USA"]
payment_methods = ["credit_card", "paypal", "bank_transfer"]
order_statuses = ["pending", "shipped", "delivered", "cancelled"]
payment_statuses = ["pending", "completed", "failed", "refunded"]

def generate_customers(n=100):
    customers = []
    for i in range(n):
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = f"{first.lower()}.{last.lower()}{random.randint(1, 100)}@example.com"
        city = random.choice(cities)
        state = random.choice(states)
        customers.append((first, last, email, f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}", f"{random.randint(100, 999)} Main St", city, state, random.choice(countries), f"{random.randint(10000, 99999)}"))
    return customers

def generate_orders(customer_ids, n=1000):
    orders = []
    for _ in range(n):
        customer_id = random.choice(customer_ids)
        total_amount = round(random.uniform(20, 500), 2)
        status = random.choice(order_statuses)
        order_date = datetime.now() - timedelta(days=random.randint(0, 365))
        orders.append((customer_id, order_date, total_amount, status, f"{random.randint(100, 999)} Shipping Ave"))
    return orders

def main():
    print("Initializing e-commerce database...")
    engine = create_engine(settings.DATABASE_URL)
    
    # Create tables
    with engine.connect() as conn:
        for statement in create_tables_sql.split(";"):
            if statement.strip():
                conn.execute(text(statement.strip()))
        conn.commit()
    print("E-commerce tables created successfully!")
    
    # Create SQLAlchemy tables (query history, saved queries, etc.)
    Base.metadata.create_all(bind=engine)
    print("SQLAlchemy tables created successfully!")
    
    # Insert categories
    with engine.connect() as conn:
        for category in categories_data:
            conn.execute(text("INSERT OR IGNORE INTO categories (category_name, description) VALUES (:name, :desc)"), {"name": category[0], "desc": category[1]})
        conn.commit()
    print("Categories inserted!")
    
    # Insert products
    with engine.connect() as conn:
        for product in products_data:
            conn.execute(text("INSERT OR IGNORE INTO products (category_id, product_name, description, price, stock_quantity, sku) VALUES (:cid, :name, :desc, :price, :stock, :sku)"), {"cid": product[0], "name": product[1], "desc": product[2], "price": product[3], "stock": product[4], "sku": product[5]})
        conn.commit()
    print("Products inserted!")
    
    # Insert customers
    customers = generate_customers(100)
    with engine.connect() as conn:
        for customer in customers:
            conn.execute(text("INSERT OR IGNORE INTO customers (first_name, last_name, email, phone, address, city, state, country, postal_code) VALUES (:fn, :ln, :email, :phone, :addr, :city, :state, :country, :zip)"), {"fn": customer[0], "ln": customer[1], "email": customer[2], "phone": customer[3], "addr": customer[4], "city": customer[5], "state": customer[6], "country": customer[7], "zip": customer[8]})
        conn.commit()
    print("Customers inserted!")
    
    # Get customer and product IDs
    with engine.connect() as conn:
        customer_ids = [row[0] for row in conn.execute(text("SELECT customer_id FROM customers")).fetchall()]
        product_results = conn.execute(text("SELECT product_id, price FROM products")).fetchall()
        product_id_to_price = {row[0]: row[1] for row in product_results}
        product_ids = list(product_id_to_price.keys())
    
    # Insert orders
    orders = generate_orders(customer_ids, 1000)
    with engine.connect() as conn:
        inserted_order_ids = []
        for order in orders:
            result = conn.execute(text("INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address) VALUES (:cid, :date, :total, :status, :addr)"), {"cid": order[0], "date": order[1], "total": order[2], "status": order[3], "addr": order[4]})
            inserted_order_ids.append(result.lastrowid)
        conn.commit()
    print("Orders inserted!")
    
    # Insert order items
    with engine.connect() as conn:
        for order_id in inserted_order_ids:
            num_items = random.randint(1, 5)
            for _ in range(num_items):
                product_id = random.choice(product_ids)
                quantity = random.randint(1, 3)
                unit_price = product_id_to_price[product_id]
                subtotal = round(unit_price * quantity, 2)
                conn.execute(text("INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES (:oid, :pid, :qty, :up, :sub)"), {"oid": order_id, "pid": product_id, "qty": quantity, "up": unit_price, "sub": subtotal})
        conn.commit()
    print("Order items inserted!")
    
    # Insert payments
    payments = []
    for order_id in inserted_order_ids:
        amount = round(random.uniform(20, 500), 2)
        payment_method = random.choice(payment_methods)
        payment_status = random.choice(payment_statuses)
        transaction_id = f"TXN-{random.randint(100000, 999999)}"
        payments.append((order_id, datetime.now() - timedelta(days=random.randint(0, 365)), amount, payment_method, payment_status, transaction_id))
    
    with engine.connect() as conn:
        for payment in payments:
            conn.execute(text("INSERT INTO payments (order_id, payment_date, amount, payment_method, payment_status, transaction_id) VALUES (:oid, :date, :amt, :method, :status, :txn)"), {"oid": payment[0], "date": payment[1], "amt": payment[2], "method": payment[3], "status": payment[4], "txn": payment[5]})
        conn.commit()
    print("Payments inserted!")
    
    # Step 3: Embed schema in ChromaDB
    print("Embedding schema in ChromaDB...")
    introspector = SchemaIntrospectionService()
    schema = introspector.get_schema()
    embedder = SchemaEmbeddingService()
    embedder.embed_schema(schema)
    print("Schema embedded successfully!")
    
    print("✅ E-commerce data initialization complete!")

if __name__ == "__main__":
    main()

