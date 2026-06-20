import pandas as pd
from dashboard.utils.db_connection import get_engine


# KPI 1 → Total Revenue
def get_total_revenue():
    engine = get_engine()

    query = """
    SELECT SUM(revenue_generated) AS revenue
    FROM sales_fact
    """

    df = pd.read_sql(query, engine)

    return round(df["revenue"][0], 2)


# KPI 2 → Total Products
def get_total_products():
    engine = get_engine()

    query = """
    SELECT COUNT(*) AS total_products
    FROM products
    """

    df = pd.read_sql(query, engine)

    return int(df["total_products"][0])


# KPI 3 → Supplier Count
def get_total_suppliers():
    engine = get_engine()

    query = """
    SELECT COUNT(DISTINCT supplier_name) AS suppliers
    FROM suppliers
    """

    df = pd.read_sql(query, engine)

    return int(df["suppliers"][0])


# KPI 4 → Average Shipping Cost
def get_avg_shipping_cost():
    engine = get_engine()

    query = """
    SELECT AVG(shipping_cost) AS avg_cost
    FROM logistics
    """

    df = pd.read_sql(query, engine)

    return round(df["avg_cost"][0], 2)