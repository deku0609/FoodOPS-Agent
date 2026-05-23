import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Restaurant AI Dashboard", layout="wide")

st.title("Restaurant Operations Dashboard")
st.markdown("Synthetic data dashboard for Mumbai Burger Cafe")

customers = pd.read_csv("data/customers.csv")
reservations = pd.read_csv("data/reservations.csv")
orders = pd.read_csv("data/orders.csv")
chat_logs = pd.read_csv("data/chat_logs.csv")

customers["join_date"] = pd.to_datetime(customers["join_date"])
reservations["booking_date"] = pd.to_datetime(reservations["booking_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])
chat_logs["chat_date"] = pd.to_datetime(chat_logs["chat_date"])

st.sidebar.header("Filters")

channel_filter = st.sidebar.multiselect(
    "Select order channel",
    options=orders["channel"].unique(),
    default=orders["channel"].unique()
)

filtered_orders = orders[orders["channel"].isin(channel_filter)]

total_revenue = filtered_orders["final_amount"].sum()
total_orders = filtered_orders["order_id"].nunique()
average_order_value = total_revenue / total_orders if total_orders > 0 else 0
total_reservations = reservations["reservation_id"].nunique()
ai_resolved_chats = (chat_logs["resolved_by_ai"] == 1).sum()
total_chats = chat_logs["chat_id"].nunique()
ai_resolution_rate = (ai_resolved_chats / total_chats) * 100 if total_chats > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders}")
col3.metric("Avg Order Value", f"₹{average_order_value:,.0f}")
col4.metric("AI Resolution Rate", f"{ai_resolution_rate:.1f}%")

filtered_orders["month"] = filtered_orders["order_date"].dt.to_period("M").astype(str)

monthly_revenue = (
    filtered_orders.groupby("month")["final_amount"]
    .sum()
    .reset_index()
)

top_items = (
    filtered_orders.groupby("item_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

revenue_by_channel = (
    filtered_orders.groupby("channel")["final_amount"]
    .sum()
    .reset_index()
)

reservation_status = (
    reservations.groupby("status")["reservation_id"]
    .count()
    .reset_index()
)

fig_line = px.line(
    monthly_revenue,
    x="month",
    y="final_amount",
    title="Monthly Revenue"
)

fig_bar = px.bar(
    top_items,
    x="item_name",
    y="quantity",
    title="Top 5 Selling Items",
    color="quantity"
)

fig_pie = px.pie(
    revenue_by_channel,
    names="channel",
    values="final_amount",
    title="Revenue by Channel"
)

fig_res = px.bar(
    reservation_status,
    x="status",
    y="reservation_id",
    title="Reservation Status Count",
    color="status"
)

chart1, chart2 = st.columns(2)
chart1.plotly_chart(fig_line, use_container_width=True)
chart2.plotly_chart(fig_bar, use_container_width=True)

chart3, chart4 = st.columns(2)
chart3.plotly_chart(fig_pie, use_container_width=True)
chart4.plotly_chart(fig_res, use_container_width=True)

st.subheader("Recent Orders")
st.dataframe(filtered_orders.head(20))