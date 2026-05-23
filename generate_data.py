import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker("en_IN")
random.seed(42)
np.random.seed(42)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

restaurant_name = "Mumbai Burger Cafe"

menu_items = [
    {"item_name": "Classic Veg Burger", "category": "Burger", "price": 149},
    {"item_name": "Cheese Burst Burger", "category": "Burger", "price": 189},
    {"item_name": "Paneer Grill Burger", "category": "Burger", "price": 209},
    {"item_name": "Fries", "category": "Sides", "price": 99},
    {"item_name": "Peri Peri Fries", "category": "Sides", "price": 119},
    {"item_name": "Cold Coffee", "category": "Beverage", "price": 129},
    {"item_name": "Chocolate Shake", "category": "Beverage", "price": 159},
    {"item_name": "Veg Wrap", "category": "Wrap", "price": 179},
    {"item_name": "Chicken Wrap", "category": "Wrap", "price": 219},
    {"item_name": "Brownie", "category": "Dessert", "price": 109},
]

query_types = [
    "table_booking",
    "menu_question",
    "delivery_delay",
    "refund_request",
    "coupon_issue",
    "order_status",
    "opening_hours",
    "party_booking",
]

def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def generate_customers(n=500):
    customers = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 3, 31)

    for i in range(1, n + 1):
        join_date = random_date(start_date, end_date)
        customer = {
            "customer_id": i,
            "customer_name": fake.name(),
            "city": "Mumbai",
            "area": random.choice(["Andheri", "Bandra", "Powai", "Dadar", "Ghatkopar", "Kurla"]),
            "phone": fake.phone_number(),
            "join_date": join_date.date(),
            "repeat_customer": random.choice([0, 1]),
            "preferred_channel": random.choice(["dine_in", "delivery", "takeaway"]),
        }
        customers.append(customer)

    return pd.DataFrame(customers)

def generate_reservations(customers_df, n=1200):
    reservations = []
    start_date = datetime(2025, 7, 1)
    end_date = datetime(2026, 3, 31)

    for i in range(1, n + 1):
        customer_id = random.choice(customers_df["customer_id"].tolist())
        booking_date = random_date(start_date, end_date)
        party_size = random.choice([1, 2, 2, 3, 4, 4, 5, 6, 8])
        time_slot = random.choice(["12:00", "13:00", "14:00", "19:00", "20:00", "21:00"])
        status = random.choices(
            ["completed", "cancelled", "no_show"],
            weights=[70, 20, 10],
            k=1
        )[0]

        reservations.append({
            "reservation_id": i,
            "customer_id": customer_id,
            "booking_date": booking_date.date(),
            "time_slot": time_slot,
            "party_size": party_size,
            "booking_source": random.choice(["website", "phone", "walk_in", "instagram"]),
            "status": status,
            "special_request": random.choice(["none", "birthday", "window_seat", "high_chair"]),
        })

    return pd.DataFrame(reservations)

def generate_orders(customers_df, n=5000):
    orders = []
    start_date = datetime(2025, 7, 1)
    end_date = datetime(2026, 3, 31)

    for i in range(1, n + 1):
        customer_id = random.choice(customers_df["customer_id"].tolist())
        order_date = random_date(start_date, end_date)
        item = random.choice(menu_items)
        quantity = random.choice([1, 1, 1, 2, 2, 3])
        is_weekend = order_date.weekday() >= 5

        if is_weekend:
            quantity += random.choice([0, 1])

        base_amount = item["price"] * quantity
        discount = random.choice([0, 0, 0, 20, 30, 50])
        final_amount = max(base_amount - discount, 50)

        orders.append({
            "order_id": i,
            "customer_id": customer_id,
            "order_date": order_date.date(),
            "item_name": item["item_name"],
            "category": item["category"],
            "quantity": quantity,
            "unit_price": item["price"],
            "gross_amount": base_amount,
            "discount": discount,
            "final_amount": final_amount,
            "channel": random.choice(["dine_in", "delivery", "takeaway"]),
            "payment_method": random.choice(["upi", "card", "cash"]),
            "prep_time_min": random.randint(10, 35),
        })

    return pd.DataFrame(orders)

def generate_chat_logs(customers_df, n=1500):
    chat_logs = []
    start_date = datetime(2025, 7, 1)
    end_date = datetime(2026, 3, 31)

    for i in range(1, n + 1):
        customer_id = random.choice(customers_df["customer_id"].tolist())
        chat_date = random_date(start_date, end_date)
        query_type = random.choice(query_types)
        resolved_by_ai = random.choices([1, 0], weights=[75, 25], k=1)[0]
        escalated = 0 if resolved_by_ai == 1 else 1
        response_time = random.randint(15, 180) if resolved_by_ai == 1 else random.randint(180, 600)

        chat_logs.append({
            "chat_id": i,
            "customer_id": customer_id,
            "chat_date": chat_date.date(),
            "query_type": query_type,
            "resolved_by_ai": resolved_by_ai,
            "escalated": escalated,
            "response_time_sec": response_time,
            "customer_sentiment": random.choice(["positive", "neutral", "negative"]),
        })

    return pd.DataFrame(chat_logs)

def main():
    customers_df = generate_customers()
    reservations_df = generate_reservations(customers_df)
    orders_df = generate_orders(customers_df)
    chat_logs_df = generate_chat_logs(customers_df)

    customers_df.to_csv(os.path.join(DATA_DIR, "customers.csv"), index=False)
    reservations_df.to_csv(os.path.join(DATA_DIR, "reservations.csv"), index=False)
    orders_df.to_csv(os.path.join(DATA_DIR, "orders.csv"), index=False)
    chat_logs_df.to_csv(os.path.join(DATA_DIR, "chat_logs.csv"), index=False)

    print(f"Data generated successfully for {restaurant_name}")
    print("Files saved in data/ folder")
    print(f"Customers: {len(customers_df)}")
    print(f"Reservations: {len(reservations_df)}")
    print(f"Orders: {len(orders_df)}")
    print(f"Chat logs: {len(chat_logs_df)}")

if __name__ == "__main__":
    main()