queries = {
    "total_sales": "SELECT SUM(sales) AS total_sales FROM sales;",
    "total_orders": "SELECT COUNT(order_id) AS total_orders FROM sales;",
    "avg_sales": "SELECT AVG(sales) AS avg_sales FROM sales;",

    "top_state": """
        SELECT state, SUM(sales) AS revenue
        FROM sales
        GROUP BY state
        ORDER BY revenue DESC
        LIMIT 1;
    """,

    "top_city": """
        SELECT city, SUM(sales) AS revenue
        FROM sales
        GROUP BY city
        ORDER BY revenue DESC
        LIMIT 1;
    """,

    "top_5_cities": """
        SELECT city, SUM(sales) AS revenue
        FROM sales
        GROUP BY city
        ORDER BY revenue DESC
        LIMIT 5;
    """,

    "monthly_sales": """
    SELECT strftime('%Y-%m', order_date) AS month, SUM(sales) AS revenue
    FROM sales
    GROUP BY month
    ORDER BY month;
    """,

    "sales_distribution": """
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
}