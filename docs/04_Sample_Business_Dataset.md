# DataNarrate - Sample Business Dataset (E-Commerce)

## Overview

This e-commerce database serves as a sample dataset for demonstrating DataNarrate's capabilities. It includes customers, products, orders, order items, payments, and categories.

---

## Table: categories

Product categories for organization.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| category_id | SERIAL | PRIMARY KEY | Unique category identifier |
| category_name | VARCHAR(100) | UNIQUE, NOT NULL | Category name |
| description | TEXT | NULL | Category description |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

---

## Table: products

Product inventory and details.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| product_id | SERIAL | PRIMARY KEY | Unique product identifier |
| category_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES categories(category_id) | Product category |
| product_name | VARCHAR(255) | NOT NULL | Product name |
| description | TEXT | NULL | Product description |
| price | DECIMAL(10,2) | NOT NULL | Product price |
| stock_quantity | INTEGER | NOT NULL, DEFAULT 0 | Available stock |
| sku | VARCHAR(50) | UNIQUE, NOT NULL | Stock keeping unit |
| is_active | BOOLEAN | NOT NULL, DEFAULT true | Product active status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

---

## Table: customers

Customer information.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| customer_id | SERIAL | PRIMARY KEY | Unique customer identifier |
| first_name | VARCHAR(100) | NOT NULL | Customer first name |
| last_name | VARCHAR(100) | NOT NULL | Customer last name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Customer email |
| phone | VARCHAR(20) | NULL | Customer phone number |
| address | TEXT | NULL | Customer address |
| city | VARCHAR(100) | NULL | City |
| state | VARCHAR(100) | NULL | State/Province |
| country | VARCHAR(100) | NULL | Country |
| postal_code | VARCHAR(20) | NULL | Postal/ZIP code |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

---

## Table: orders

Customer orders.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| order_id | SERIAL | PRIMARY KEY | Unique order identifier |
| customer_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES customers(customer_id) | Customer who placed the order |
| order_date | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Order date |
| total_amount | DECIMAL(10,2) | NOT NULL | Total order amount |
| status | VARCHAR(50) | NOT NULL, DEFAULT 'pending' | Order status (pending, shipped, delivered, cancelled) |
| shipping_address | TEXT | NULL | Shipping address |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

---

## Table: order_items

Individual items within each order.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| order_item_id | SERIAL | PRIMARY KEY | Unique order item identifier |
| order_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES orders(order_id) | Associated order |
| product_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES products(product_id) | Product in order |
| quantity | INTEGER | NOT NULL, DEFAULT 1 | Quantity ordered |
| unit_price | DECIMAL(10,2) | NOT NULL | Price per unit at time of order |
| subtotal | DECIMAL(10,2) | NOT NULL | Line item subtotal |

---

## Table: payments

Payment transactions for orders.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| payment_id | SERIAL | PRIMARY KEY | Unique payment identifier |
| order_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES orders(order_id) | Associated order |
| payment_date | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Payment date |
| amount | DECIMAL(10,2) | NOT NULL | Payment amount |
| payment_method | VARCHAR(50) | NOT NULL | Payment method (credit_card, paypal, bank_transfer, etc.) |
| payment_status | VARCHAR(50) | NOT NULL, DEFAULT 'pending' | Payment status (pending, completed, failed, refunded) |
| transaction_id | VARCHAR(255) | NULL | External transaction ID |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

---

## Relationships

```
categories (1) ----< (N) products
customers (1) ----< (N) orders
orders (1) ----< (N) order_items
products (1) ----< (N) order_items
orders (1) ----< (N) payments
```

## Entity Relationships Summary

- **categories → products**: One category can have many products
- **customers → orders**: One customer can place many orders
- **orders → order_items**: One order can have many items
- **products → order_items**: One product can be in many order items
- **orders → payments**: One order can have multiple payment attempts/records

## Indexes

```sql
-- Products indexes
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_is_active ON products(is_active);

-- Customers indexes
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_country ON customers(country);

-- Orders indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date DESC);
CREATE INDEX idx_orders_status ON orders(status);

-- Order items indexes
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Payments indexes
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_payment_date ON payments(payment_date DESC);
CREATE INDEX idx_payments_status ON payments(payment_status);
```
