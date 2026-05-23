import pandas as pd

customers = pd.read_csv("data/customers.csv")
reservations = pd.read_csv("data/reservations.csv")
orders = pd.read_csv("data/orders.csv")
chat_logs = pd.read_csv("data/chat_logs.csv")

customers["join_date"] = pd.to_datetime(customers["join_date"])
reservations["booking_date"] = pd.to_datetime(reservations["booking_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])
chat_logs["chat_date"] = pd.to_datetime(chat_logs["chat_date"])

total_revenue = orders["final_amount"].sum()
total_orders = orders["order_id"].nunique()
average_order_value = total_revenue / total_orders

total_reservations = reservations["reservation_id"].nunique()
completed_reservations = (reservations["status"] == "completed").sum()
cancelled_reservations = (reservations["status"] == "cancelled").sum()
no_show_reservations = (reservations["status"] == "no_show").sum()

ai_resolved_chats = (chat_logs["resolved_by_ai"] == 1).sum()
total_chats = chat_logs["chat_id"].nunique()
ai_resolution_rate = (ai_resolved_chats / total_chats) * 100

top_items = (
    orders.groupby("item_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

revenue_by_channel = (
    orders.groupby("channel")["final_amount"]
    .sum()
    .sort_values(ascending=False)
)

orders["month"] = orders["order_date"].dt.to_period("M").astype(str)
monthly_revenue = (
    orders.groupby("month")["final_amount"]
    .sum()
    .reset_index()
)

print("\n--- DATA CHECK ---")
print("Customers shape:", customers.shape)
print("Reservations shape:", reservations.shape)
print("Orders shape:", orders.shape)
print("Chat logs shape:", chat_logs.shape)

print("\n--- KPI SUMMARY ---")
print("Total Revenue:", round(total_revenue, 2))
print("Total Orders:", total_orders)
print("Average Order Value:", round(average_order_value, 2))
print("Total Reservations:", total_reservations)
print("Completed Reservations:", completed_reservations)
print("Cancelled Reservations:", cancelled_reservations)
print("No-show Reservations:", no_show_reservations)
print("AI Resolution Rate:", round(ai_resolution_rate, 2), "%")

print("\n--- TOP 5 ITEMS ---")
print(top_items)

print("\n--- REVENUE BY CHANNEL ---")
print(revenue_by_channel)

print("\n--- MONTHLY REVENUE ---")
print(monthly_revenue.head(10))