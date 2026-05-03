import streamlit as st
import sqlite3
import pandas as pd
from main import get_response

st.set_page_config(page_title="Customer Dashboard", layout="wide")

st.title("📊 Customer Insights Dashboard")

st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", f"{get_response('total sales').iloc[0,0]:,.0f}")

with col2:
    st.metric("Total Orders", get_response("total orders").iloc[0,0])

with col3:
    st.metric("Avg Sales", round(get_response("average").iloc[0,0], 2))

st.markdown("---")

# --- Filter Section ---
st.markdown("## 🔎 Filters")

def get_states():
    conn = sqlite3.connect("database/sales.db")
    df = pd.read_sql_query("SELECT DISTINCT state FROM sales", conn)
    conn.close()
    return df["state"].tolist()

states = get_states()

state_filter = st.selectbox("Select State", ["All"] + states)


st.markdown("---")


# ===================== CHART SECTION START =====================

# --- Sales Trend ---
st.subheader("📈 Sales Trend")

conn = sqlite3.connect("database/sales.db")

if state_filter == "All":
    trend_query = """
    SELECT strftime('%Y-%m', order_date) AS month, SUM(sales) AS revenue
    FROM sales
    GROUP BY month
    ORDER BY month;
    """
else:
    trend_query = f"""
    SELECT strftime('%Y-%m', order_date) AS month, SUM(sales) AS revenue
    FROM sales
    WHERE state = '{state_filter}'
    GROUP BY month
    ORDER BY month;
    """

trend = pd.read_sql_query(trend_query, conn)
st.line_chart(trend.set_index("month"))


# --- Top Cities ---
st.subheader("🏙 Top Cities")

if state_filter == "All":
    cities_query = """
    SELECT city, SUM(sales) as revenue
    FROM sales
    GROUP BY city
    ORDER BY revenue DESC
    LIMIT 5;
    """
else:
    cities_query = f"""
    SELECT city, SUM(sales) as revenue
    FROM sales
    WHERE state = '{state_filter}'
    GROUP BY city
    ORDER BY revenue DESC
    LIMIT 5;
    """

cities = pd.read_sql_query(cities_query, conn)
st.bar_chart(cities.set_index("city"))


# --- Sales Distribution ---
st.subheader("📊 Sales Distribution")

if state_filter == "All":
    dist_query = """
    SELECT 
        CASE 
            WHEN sales < 500 THEN 'Low'
            WHEN sales BETWEEN 500 AND 1000 THEN 'Medium'
            ELSE 'High'
        END AS category,
        COUNT(*) AS orders
    FROM sales
    GROUP BY category;
    """
else:
    dist_query = f"""
    SELECT 
        CASE 
            WHEN sales < 500 THEN 'Low'
            WHEN sales BETWEEN 500 AND 1000 THEN 'Medium'
            ELSE 'High'
        END AS category,
        COUNT(*) AS orders
    FROM sales
    WHERE state = '{state_filter}'
    GROUP BY category;
    """

dist = pd.read_sql_query(dist_query, conn)
st.bar_chart(dist.set_index("category"))

conn.close()

# ===================== CHART SECTION END =====================


st.markdown("---")


# --- Query Section ---
st.subheader("🔍 Ask Custom Question")

user_query = st.text_input("Type your question here:")

if user_query:
    result = get_response(user_query)

    if isinstance(result, str):
        st.write(result)
    else:
        st.dataframe(result)