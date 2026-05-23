import streamlit as st
import pandas as pd

st.set_page_config(page_title="Restaurant AI Assistant", layout="wide")
st.title("Restaurant AI Assistant")
st.markdown("Offline assistant using restaurant data and rule-based responses.")

customers = pd.read_csv("data/customers.csv")
reservations = pd.read_csv("data/reservations.csv")
orders = pd.read_csv("data/orders.csv")
chat_logs = pd.read_csv("data/chat_logs.csv")

orders["order_date"] = pd.to_datetime(orders["order_date"])
reservations["booking_date"] = pd.to_datetime(reservations["booking_date"])
chat_logs["chat_date"] = pd.to_datetime(chat_logs["chat_date"])

total_revenue = orders["final_amount"].sum()
total_orders = orders["order_id"].nunique()
average_order_value = total_revenue / total_orders if total_orders > 0 else 0

top_items = (
    orders.groupby("item_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

reservation_status = (
    reservations.groupby("status")["reservation_id"]
    .count()
    .to_dict()
)

revenue_by_channel = (
    orders.groupby("channel")["final_amount"]
    .sum()
    .to_dict()
)

ai_resolved_chats = (chat_logs["resolved_by_ai"] == 1).sum()
total_chats = chat_logs["chat_id"].nunique()
ai_resolution_rate = (ai_resolved_chats / total_chats) * 100 if total_chats > 0 else 0

restaurant_policy = {
    "opening_hours": "Mumbai Burger Cafe is open every day from 11:00 AM to 11:00 PM.",
    "delivery_zones": "We deliver in Andheri, Bandra, Powai, Dadar, Ghatkopar, and Kurla.",
    "booking_policy": "Online table bookings are accepted for up to 8 people.",
    "cancellation_policy": "Reservations can be cancelled up to 2 hours before the booking time.",
    "refund_policy": "Refunds are considered only for failed payments or incorrect orders.",
    "escalation_policy": "Refunds, allergy issues, legal complaints, and sensitive issues should be escalated to a human manager."
}

def get_bot_response(user_input):
    text = user_input.lower()

    if "hello" in text or "hi" in text or "hey" in text:
        return "Hi! You can ask me about bookings, orders, revenue, top-selling items, or restaurant policies."

    if "opening" in text or "hours" in text or "timing" in text:
        return restaurant_policy["opening_hours"]

    if "delivery" in text or "zones" in text or "area" in text:
        return restaurant_policy["delivery_zones"]

    if "booking" in text or "reservation" in text:
        if "cancel" in text:
            return restaurant_policy["cancellation_policy"]
        return (
            f"{restaurant_policy['booking_policy']} "
            f"Current reservation counts are: {reservation_status}."
        )

    if "refund" in text:
        return (
            f"{restaurant_policy['refund_policy']} "
            f"{restaurant_policy['escalation_policy']}"
        )

    if "allergy" in text or "legal" in text or "complaint" in text:
        return restaurant_policy["escalation_policy"]

    if "revenue" in text or "sales" in text:
        return f"Total revenue is ₹{total_revenue:,.2f}."

    if "orders" in text and "total" in text:
        return f"Total number of orders is {total_orders}."

    if "average order value" in text or "aov" in text:
        return f"Average order value is ₹{average_order_value:,.2f}."

    if "top item" in text or "best selling" in text or "top selling" in text or "popular item" in text:
        top_items_text = "\n".join([f"- {item}: {qty}" for item, qty in top_items.items()])
        return f"Top selling items are:\n{top_items_text}"

    if "channel" in text or "dine" in text or "takeaway" in text or "delivery revenue" in text:
        channel_text = "\n".join([f"- {channel}: ₹{amount:,.2f}" for channel, amount in revenue_by_channel.items()])
        return f"Revenue by channel is:\n{channel_text}"

    if "ai" in text or "chat" in text or "support" in text:
        return f"AI resolution rate is {ai_resolution_rate:.2f}%."

    if "cancelled reservation" in text or "no show" in text or "completed reservation" in text:
        return f"Reservation status summary: {reservation_status}"

    return "I do not have enough information to answer that yet. Please ask about bookings, revenue, orders, top items, delivery zones, refunds, or support metrics."

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! Ask me about restaurant bookings, operations, menu trends, or support metrics."
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question about the restaurant")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    answer = get_bot_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})