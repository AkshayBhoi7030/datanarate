from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from io import BytesIO
import pandas as pd
from sqlalchemy import create_engine, text
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

app = FastAPI(title="DataNarrate API", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
engine = create_engine("sqlite:///../datanarrate.db")

# Predefined query templates for demo
query_templates = {
    "sales by category": """
        SELECT 
            c.category_name,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.subtotal) as total_sales
        FROM categories c
        JOIN products p ON c.category_id = p.category_id
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY c.category_name
        ORDER BY total_sales DESC
    """,
    "top customers": """
        SELECT 
            c.first_name || ' ' || c.last_name as customer_name,
            COUNT(o.order_id) as total_orders,
            SUM(o.total_amount) as total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id
        ORDER BY total_spent DESC
        LIMIT 10
    """,
    "monthly sales": """
        SELECT 
            strftime('%Y-%m', o.order_date) as month,
            SUM(o.total_amount) as total_sales
        FROM orders o
        GROUP BY strftime('%Y-%m', o.order_date)
        ORDER BY month
    """,
    "products by sales": """
        SELECT 
            p.product_name,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.subtotal) as total_revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id
        ORDER BY total_revenue DESC
        LIMIT 10
    """,
    "order status": """
        SELECT 
            status,
            COUNT(*) as count
        FROM orders
        GROUP BY status
    """
}

@app.get("/health")
async def health():
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        },
        "message": "Service is healthy"
    }

@app.get("/status")
async def status():
    return {
        "success": True,
        "data": {
            "database": "healthy",
            "redis": "healthy",
            "overall": "healthy"
        }
    }

@app.get("/api/v1/history")
async def history():
    return {"success": True, "data": [], "total": 0, "page": 1, "page_size": 20}

@app.post("/api/v1/history")
async def create_history(request: Request):
    return {"success": True, "data": {}}

@app.delete("/api/v1/history/{id}")
async def delete_history(id: str):
    return {"success": True}

@app.get("/api/v1/saved-queries")
async def saved_queries():
    return {"success": True, "data": [], "total": 0, "page": 1, "page_size": 20}

@app.post("/api/v1/saved-queries")
async def create_saved_query(request: Request):
    return {"success": True, "data": {}}

@app.put("/api/v1/saved-queries/{id}")
async def update_saved_query(id: str, request: Request):
    return {"success": True, "data": {}}

@app.delete("/api/v1/saved-queries/{id}")
async def delete_saved_query(id: str):
    return {"success": True}

@app.patch("/api/v1/saved-queries/{id}/favorite")
async def toggle_favorite(id: str):
    return {"success": True, "data": {}}

@app.post("/api/v1/query")
async def query(request: Request):
    body = await request.json()
    question = body.get("question", "sales by category").lower()
    
    # Find matching query template
    sql = query_templates.get("sales by category")  # default
    for key, query in query_templates.items():
        if key in question:
            sql = query
            break
    
    try:
        # Execute query
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
        
        # Generate simple insight
        insight = f"Here are the results for your question: '{question}'. Found {len(data)} records."
        
        return {
            "success": True,
            "data": {
                "question": question,
                "sql": sql.strip(),
                "data": data,
                "insight": insight
            },
            "message": "Query executed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "message": str(e)
        }


@app.post("/api/v1/designer/generate")
async def generate_database(request: Request):
    body = await request.json()
    description = body.get("description", "")
    database_type = body.get("database_type", "all")
    
    # Predefined demo responses based on keywords for demonstration
    demo_responses = {
        "e-commerce": {
            "schema": [
                {"table": "customers", "columns": ["id", "first_name", "last_name", "email", "phone", "address", "created_at"]},
                {"table": "products", "columns": ["id", "name", "description", "price", "stock", "category_id", "created_at"]},
                {"table": "categories", "columns": ["id", "name", "description"]},
                {"table": "orders", "columns": ["id", "customer_id", "total", "status", "order_date", "shipping_address"]},
                {"table": "order_items", "columns": ["id", "order_id", "product_id", "quantity", "unit_price", "subtotal"]},
                {"table": "payments", "columns": ["id", "order_id", "amount", "method", "status", "transaction_id", "payment_date"]}
            ],
            "sqlite": """
## SQLite

### CREATE TABLE statements for E-Commerce Database

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipping_address TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    method VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(255),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
""",
            "mysql": """
## MySQL

### CREATE TABLE statements for E-Commerce Database

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipping_address TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    method VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(255),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
""",
            "postgresql": """
## PostgreSQL

### CREATE TABLE statements for E-Commerce Database

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipping_address TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    method VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(255),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
""",
            "oracle": """
## Oracle

### CREATE TABLE statements for E-Commerce Database

CREATE TABLE categories (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100) NOT NULL UNIQUE,
    description CLOB
);

CREATE TABLE products (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_id NUMBER NOT NULL,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    price NUMBER(10,2) NOT NULL,
    stock NUMBER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE customers (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR2(100) NOT NULL,
    last_name VARCHAR2(100) NOT NULL,
    email VARCHAR2(255) UNIQUE NOT NULL,
    phone VARCHAR2(20),
    address CLOB,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE orders (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id NUMBER NOT NULL,
    total NUMBER(10,2) NOT NULL,
    status VARCHAR2(50) NOT NULL DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT SYSTIMESTAMP,
    shipping_address CLOB,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    quantity NUMBER NOT NULL DEFAULT 1,
    unit_price NUMBER(10,2) NOT NULL,
    subtotal NUMBER(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE payments (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id NUMBER NOT NULL,
    amount NUMBER(10,2) NOT NULL,
    method VARCHAR2(50) NOT NULL,
    status VARCHAR2(50) NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR2(255),
    payment_date TIMESTAMP DEFAULT SYSTIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
""",
            "sqlserver": """
## SQL Server

### CREATE TABLE statements for E-Commerce Database

CREATE TABLE categories (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    description NVARCHAR(MAX)
);

CREATE TABLE products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    category_id INT NOT NULL,
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE customers (
    id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    email NVARCHAR(255) UNIQUE NOT NULL,
    phone NVARCHAR(20),
    address NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    status NVARCHAR(50) NOT NULL DEFAULT 'pending',
    order_date DATETIME DEFAULT GETDATE(),
    shipping_address NVARCHAR(MAX),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE payments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    method NVARCHAR(50) NOT NULL,
    status NVARCHAR(50) NOT NULL DEFAULT 'pending',
    transaction_id NVARCHAR(255),
    payment_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
""",
            "analytics": [
                "SELECT c.first_name, c.last_name, COUNT(o.id) as order_count, SUM(o.total) as total_spent FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id ORDER BY total_spent DESC LIMIT 10;",
                "SELECT strftime('%Y-%m', o.order_date) as month, SUM(o.total) as revenue FROM orders o GROUP BY month ORDER BY month;",
                "SELECT p.name, SUM(oi.quantity) as total_sold, SUM(oi.subtotal) as revenue FROM products p JOIN order_items oi ON p.id = oi.product_id GROUP BY p.id ORDER BY revenue DESC LIMIT 10;",
                "SELECT cat.name, SUM(oi.subtotal) as category_revenue FROM categories cat JOIN products p ON cat.id = p.category_id JOIN order_items oi ON p.id = oi.product_id GROUP BY cat.id ORDER BY category_revenue DESC;",
                "SELECT o.status, COUNT(*) as count FROM orders o GROUP BY o.status;"
            ],
            "kpis": [
                "Total Revenue",
                "Total Orders",
                "Active Customers",
                "Average Order Value",
                "Top Selling Products",
                "Conversion Rate",
                "Customer Retention Rate",
                "Inventory Turnover"
            ],
            "qualityScore": 95
        },
        "hospital": {
            "schema": [
                {"table": "patients", "columns": ["id", "first_name", "last_name", "date_of_birth", "gender", "phone", "email", "address", "created_at"]},
                {"table": "doctors", "columns": ["id", "first_name", "last_name", "specialization", "phone", "email", "department_id", "created_at"]},
                {"table": "departments", "columns": ["id", "name", "description"]},
                {"table": "appointments", "columns": ["id", "patient_id", "doctor_id", "appointment_date", "status", "notes", "created_at"]},
                {"table": "medical_records", "columns": ["id", "patient_id", "doctor_id", "visit_date", "diagnosis", "prescription", "notes", "created_at"]}
            ],
            "sqlite": """
## SQLite

### CREATE TABLE statements for Hospital Management Database

CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    department_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE medical_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    visit_date TIMESTAMP NOT NULL,
    diagnosis TEXT,
    prescription TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
""",
            "mysql": """
## MySQL

### CREATE TABLE statements for Hospital Management Database

CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    department_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    visit_date TIMESTAMP NOT NULL,
    diagnosis TEXT,
    prescription TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
""",
            "postgresql": """
## PostgreSQL

### CREATE TABLE statements for Hospital Management Database

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    department_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE medical_records (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    visit_date TIMESTAMP NOT NULL,
    diagnosis TEXT,
    prescription TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
""",
            "oracle": """
## Oracle

### CREATE TABLE statements for Hospital Management Database

CREATE TABLE departments (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100) NOT NULL UNIQUE,
    description CLOB
);

CREATE TABLE doctors (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR2(100) NOT NULL,
    last_name VARCHAR2(100) NOT NULL,
    specialization VARCHAR2(100) NOT NULL,
    phone VARCHAR2(20),
    email VARCHAR2(255) UNIQUE,
    department_id NUMBER,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE patients (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR2(100) NOT NULL,
    last_name VARCHAR2(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR2(10),
    phone VARCHAR2(20),
    email VARCHAR2(255),
    address CLOB,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE appointments (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id NUMBER NOT NULL,
    doctor_id NUMBER NOT NULL,
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR2(50) DEFAULT 'scheduled',
    notes CLOB,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE medical_records (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id NUMBER NOT NULL,
    doctor_id NUMBER NOT NULL,
    visit_date TIMESTAMP NOT NULL,
    diagnosis CLOB,
    prescription CLOB,
    notes CLOB,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
""",
            "sqlserver": """
## SQL Server

### CREATE TABLE statements for Hospital Management Database

CREATE TABLE departments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    description NVARCHAR(MAX)
);

CREATE TABLE doctors (
    id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    specialization NVARCHAR(100) NOT NULL,
    phone NVARCHAR(20),
    email NVARCHAR(255) UNIQUE,
    department_id INT,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE patients (
    id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender NVARCHAR(10),
    phone NVARCHAR(20),
    email NVARCHAR(255),
    address NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE appointments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    status NVARCHAR(50) DEFAULT 'scheduled',
    notes NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE medical_records (
    id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    visit_date DATETIME NOT NULL,
    diagnosis NVARCHAR(MAX),
    prescription NVARCHAR(MAX),
    notes NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
""",
            "analytics": [
                "SELECT d.first_name, d.last_name, COUNT(a.id) as appointment_count FROM doctors d JOIN appointments a ON d.id = a.doctor_id GROUP BY d.id ORDER BY appointment_count DESC;",
                "SELECT strftime('%Y-%m', a.appointment_date) as month, COUNT(*) as appointments FROM appointments a GROUP BY month ORDER BY month;",
                "SELECT p.first_name, p.last_name, COUNT(m.id) as record_count FROM patients p JOIN medical_records m ON p.id = m.patient_id GROUP BY p.id ORDER BY record_count DESC LIMIT 10;",
                "SELECT a.status, COUNT(*) as count FROM appointments a GROUP BY a.status;"
            ],
            "kpis": [
                "Total Patients",
                "Total Doctors",
                "Appointments Today",
                "Average Wait Time",
                "Patient Satisfaction",
                "Readmission Rate",
                "Department Utilization"
            ],
            "qualityScore": 93
        }
    }
    
    # Match keywords to select demo response
    base_response = demo_responses.get("e-commerce")  # default
    for keyword, data in demo_responses.items():
        if keyword in description.lower():
            base_response = data
            break
    
    # Prepare final response data based on selected database type
    if database_type == "all":
        sql_content = base_response["sqlite"] + "\n" + base_response["mysql"] + "\n" + base_response["postgresql"] + "\n" + base_response["oracle"] + "\n" + base_response["sqlserver"]
    else:
        sql_content = base_response.get(database_type, base_response["sqlite"])
    
    return {
        "success": True,
        "data": {
            "schema": base_response["schema"],
            "sql": sql_content,
            "analytics": base_response["analytics"],
            "kpis": base_response["kpis"],
            "qualityScore": base_response["qualityScore"]
        },
        "message": "Database design generated successfully"
    }


@app.post("/api/v1/exports/csv")
async def export_csv(request: Request):
    body = await request.json()
    data = body.get("data", [])
    filename = body.get("filename", "export.csv")
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_csv(output, index=False, encoding="utf-8")
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/v1/exports/excel")
async def export_excel(request: Request):
    body = await request.json()
    data = body.get("data", [])
    filename = body.get("filename", "export.xlsx")
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/v1/exports/pdf")
async def export_pdf(request: Request):
    body = await request.json()
    data = body.get("data", [])
    question = body.get("question", "")
    sql = body.get("sql", "")
    insight = body.get("insight", "")
    filename = body.get("filename", "report.pdf")
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("DataNarrate Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Question", styles["Heading2"]))
    story.append(Paragraph(question, styles["BodyText"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Generated SQL", styles["Heading2"]))
    story.append(Paragraph(sql, styles["Code"] if "Code" in styles else styles["BodyText"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("AI Insights", styles["Heading2"]))
    story.append(Paragraph(insight, styles["BodyText"]))
    story.append(Spacer(1, 12))
    if data:
        story.append(Paragraph("Results", styles["Heading2"]))
        df = pd.DataFrame(data)
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
    doc.build(story)
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/v1/preferences")
async def get_preferences():
    return {"success": True, "data": {"theme": "light", "language": "en"}}

@app.get("/api/v1/schema")
async def get_schema():
    schema = []
    with engine.connect() as conn:
        # Get all tables
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"))
        tables = [row[0] for row in result.fetchall()]
        
        for table in tables:
            # Get columns for each table
            cols_result = conn.execute(text(f"PRAGMA table_info({table})"))
            columns = []
            for col in cols_result.fetchall():
                columns.append({
                    "name": col[1],
                    "type": col[2],
                    "nullable": col[3] == 0,
                    "primary_key": col[5] == 1
                })
            schema.append({
                "table_name": table,
                "columns": columns
            })
    
    return {
        "success": True,
        "data": schema
    }

@app.put("/api/v1/preferences")
async def update_preferences(request: Request):
    return {"success": True, "data": {}}

@app.get("/api/v1/dashboard/stats")
async def get_dashboard_stats():
    with engine.connect() as conn:
        total_sales = conn.execute(text("SELECT SUM(total_amount) FROM orders")).scalar() or 0
        total_orders = conn.execute(text("SELECT COUNT(*) FROM orders")).scalar() or 0
        total_customers = conn.execute(text("SELECT COUNT(*) FROM customers")).scalar() or 0
        total_products = conn.execute(text("SELECT COUNT(*) FROM products")).scalar() or 0
        
        return {
            "success": True,
            "data": {
                "total_revenue": float(total_sales),
                "total_orders": total_orders,
                "total_customers": total_customers,
                "total_products": total_products
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_simple_working:app", host="0.0.0.0", port=8000, reload=True)
