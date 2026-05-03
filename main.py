import sqlite3
import pandas as pd
import re

from scripts.queries import queries


def run_query(query):
    conn = sqlite3.connect("database/sales.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_response(user_input):
    user_input = user_input.lower()

    match = re.search(r'\d+', user_input)
    limit = match.group() if match else "5"

    if "lowest" in user_input or "least" in user_input:
        order = "ASC"
    else:
        order = "DESC"

    if "city" in user_input:
        query = f"""
        SELECT city, SUM(sales) as revenue
        FROM sales
        GROUP BY city
        ORDER BY revenue {order}
        LIMIT {limit};
        """
        return run_query(query)
    
    if "top" in user_input and "city" in user_input:
        query = f"""
        SELECT city, SUM(sales) as revenue
        FROM sales
        GROUP BY city
        ORDER BY revenue DESC
        LIMIT {limit};
        """
        return run_query(query)
    
    elif "total sales" in user_input:
        return run_query(queries["total_sales"])

    elif "total orders" in user_input:
        return run_query(queries["total_orders"])

    elif "average" in user_input:
        return run_query(queries["avg_sales"])

    elif "state" in user_input:
        return run_query(queries["top_state"])

    elif "top city" in user_input:
        return run_query(queries["top_city"])

    elif "top 5 cities" in user_input:
        return run_query(queries["top_5_cities"])

    elif "monthly" in user_input or "trend" in user_input:
        return run_query(queries["monthly_sales"])

    elif "distribution" in user_input:
        return run_query(queries["sales_distribution"])

    else:
        return "Try asking about sales, orders, cities, or trends."
