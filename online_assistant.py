import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="FoodOPS Agent Online", layout="wide")
st.title("FoodOPS Agent - Online Assistant")
st.markdown("LLM-powered restaurant assistant using live CSV data and grounded context.")

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("OPENROUTER_API_KEY not found. Add it to your .env file.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "FoodOPS Agent"
    }
)

orders = pd.read_csv("data/orders.csv")
reservations = pd.read_csv("data/reservations.csv")
chat_logs = pd.read_csv("data/chat_logs.csv")
customers = pd.read_csv("data/customers.csv")

orders["order_date"] = pd.to_datetime(orders["order_date"])
reservations["booking_date"] = pd.to_datetime(reservations["booking_date"])
chat_logs["chat_date"] = pd.to_datetime(chat_logs["chat_date"])
customers["join_date"] = pd.to_datetime(customers["join_date"])

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
    "escalation_policy": "Refunds, allergy issues, legal complaints, private customer data requests, and sensitive issues should be escalated to a human manager."
}

def build_context():
    top_items_text = "\n".join([f"- {item}: {qty}" for item, qty in top_items.items()])
    reservation_text = "\n".join([f"- {status}: {count}" for status, count in reservation_status.items()])
    channel_text = "\n".join([f"- {channel}: ₹{amount:,.2f}" for channel, amount in revenue_by_channel.items()])

    context = f"""
Restaurant Name: Mumbai Burger Cafe

Policies:
- Opening Hours: {restaurant_policy['opening_hours']}
- Delivery Zones: {restaurant_policy['delivery_zones']}
- Booking Policy: {restaurant_policy['booking_policy']}
- Cancellation Policy: {restaurant_policy['cancellation_policy']}
- Refund Policy: {restaurant_policy['refund_policy']}
- Escalation Policy: {restaurant_policy['escalation_policy']}

Business Metrics:
- Total Revenue: ₹{total_revenue:,.2f}
- Total Orders: {total_orders}
- Average Order Value: ₹{average_order_value:,.2f}
- AI Resolution Rate: {ai_resolution_rate:.2f}%

Top Selling Items:
{top_items_text}

Reservation Status Summary:
{reservation_text}

Revenue by Channel:
{channel_text}
"""
    return context.strip()

def guardrail_response(user_input):
    text = user_input.lower()

    if "allergy" in text or "legal" in text or "complaint" in text:
        return restaurant_policy["escalation_policy"]

    if "private customer" in text or "customer phone" in text or "customer email" in text:
        return "I cannot share private customer information. Please contact a human manager for authorized access."

    if "outside mumbai" in text or "other city" in text or "other cities" in text:
        return "I only have information about our listed delivery zones in Mumbai. For delivery outside Mumbai, please contact the restaurant directly."

    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]

    if ("revenue" in text or "sales" in text) and any(month in text for month in months):
        return "I currently support total revenue only. Month-specific revenue is not available in this version yet."

    return None

def get_llm_response(user_input):
    blocked = guardrail_response(user_input)
    if blocked:
        return blocked

    context = build_context()

    system_prompt = f"""
You are FoodOPS Agent, a restaurant operations assistant for Mumbai Burger Cafe.

Rules:
1. Answer only using the provided context.
2. If the answer is not clearly available in the context, say you do not have enough information.
3. Do not invent numbers, policies, delivery areas, or customer data.
4. Escalate allergy issues, legal complaints, refunds with disputes, and private customer data requests to a human manager.
5. Keep answers clear, short, and professional.
6. If asked about unsupported analytics such as month-specific revenue, say it is not available in this version.

Context:
{context}
""".strip()

    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I’m FoodOPS Agent. Ask me about restaurant operations, revenue, orders, bookings, top items, refunds, or support performance."
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask FoodOPS Agent a question")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        answer = get_llm_response(prompt)
    except Exception as e:
        answer = f"Something went wrong while contacting the model API: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})