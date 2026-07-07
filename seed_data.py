import sqlite3
import random
from datetime import datetime, timedelta


def seed_initial_data(db_path):
    random.seed(42)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        age_group TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP)
    """)

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            items TEXT,
            total_amount INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
    """)
    conn.commit()

    # Fake Customers
    customers = [
        ("Tony",     "9876543210", "18-25"),
        ("Bruce",    "9876543211", "18-25"),
        ("Peter",    "9876543212", "13-17"),
        ("Wanda",    "9876543213", "13-17"),
        ("Wade",     "9876543214", "Under 13"),
        ("John",     "9876543215", "18-25"),
        ("Kevin",    "9876543216", "18-25"),
        ("Charles",  "9876543217", "36-50"),
        ("Max",      "9876543218", "50+"),
        ("Dua",      "9876543219", "13-17"),
        ("Ana",      "9876543220", "26-35"),
        ("Joe",      "9876543221", "13-17"),
        ("Logan",    "9876543222", "26-35"),
        ("Steven",   "9876543223", "26-35"),
        ("Meagan",   "9876543224", "13-17"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO customers (name, phone, age_group) VALUES (?,?,?)",
        customers
    )
    conn.commit()

    # Get customer IDs
    cursor.execute("SELECT customer_id FROM customers")
    customer_ids = [row[0] for row in cursor.fetchall()]

    # Menu with prices
    prices = {
        "Company Burgers": 120,
        "Frenchie Fries": 100,
        "Nuggets of Chicken": 180,
        "Coke Ka Cola": 100,
        "Soft C Softy": 80,
        "Veggie Veg Burger": 90
    }

    # Natural item combos with weights (realistic patterns for Apriori to find)
    combos = [
    # Burger + Fries + Coke: the shop's signature combo
    (["Company Burgers", "Frenchie Fries", "Coke Ka Cola"], 32),
    (["Company Burgers", "Frenchie Fries"], 2),
    (["Company Burgers"], 4),
    (["Frenchie Fries"], 3),

    # Veg Burger + Nuggets + Softy: popular pairing among the veg/snack crowd
    (["Veggie Veg Burger", "Nuggets of Chicken", "Soft C Softy"], 20),
    (["Veggie Veg Burger", "Nuggets of Chicken"], 4),
    (["Veggie Veg Burger"], 3),
    (["Nuggets of Chicken"], 3),

    # Occasional cross-combo orders for variety
    (["Frenchie Fries", "Veggie Veg Burger"], 3),
    (["Company Burgers", "Nuggets of Chicken"], 3),
    (["Nuggets of Chicken", "Frenchie Fries"], 2),
    
    ]

    # Build weighted order pool
    order_pool = []
    for combo, weight in combos:
        order_pool.extend([combo] * weight)

    # Generate 110 orders
    base_date = datetime.now() - timedelta(days=10)

    for i in range(110):
        customer_id = random.choice(customer_ids)
        items = random.choice(order_pool)
        total = sum(prices[item] for item in items)
        timestamp = base_date + timedelta(
            days=random.randint(0, 9),
            hours=random.randint(10, 22), # 10 AM-10 PM: shop's business hours
            minutes=random.randint(0, 59)
        )

        cursor.execute(
            "INSERT INTO orders (customer_id, items, total_amount, timestamp) VALUES (?,?,?,?)",
            (customer_id, ",".join(items), total, timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        )

    conn.commit()
    conn.close()
