from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
import pandas as pd

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PostgreSQL connection
engine = create_engine(
    "postgresql://admin:admin123@localhost:5432/supplychain"
)


@app.get("/")
def home():
    return {
        "message": "SupplySense API Running"
    }


@app.get("/revenue")
def revenue():
    query = """
    SELECT SUM(revenue_generated) AS revenue
    FROM sales_fact
    """

    df = pd.read_sql(query, engine)

    # temporary fixed conversion
    usd_to_inr = 95
    revenue_inr = float(df["revenue"][0]) * usd_to_inr

    return {
        "revenue": round(revenue_inr, 2)
    }


@app.get("/products")
def products():
    query = """
    SELECT COUNT(*) AS products
    FROM products
    """

    df = pd.read_sql(query, engine)

    return {
        "products": int(df["products"][0])
    }


@app.get("/suppliers")
def suppliers():
    query = """
    SELECT COUNT(*) AS suppliers
    FROM suppliers
    """

    df = pd.read_sql(query, engine)

    return {
        "suppliers": int(df["suppliers"][0])
    }


@app.get("/shipping-cost")
def shipping_cost():
    query = """
    SELECT AVG(shipping_cost) AS avg_cost
    FROM logistics
    """

    df = pd.read_sql(query, engine)

    usd_to_inr = 95
    shipping_inr = float(df["avg_cost"][0]) * usd_to_inr

    return {
        "avg_cost": round(shipping_inr, 2)
    }


@app.get("/inventory-score")
def inventory_score():
    query = """
    SELECT AVG(availability) AS score
    FROM inventory
    """

    df = pd.read_sql(query, engine)

    return {
        "score": round(float(df["score"][0]), 2)
    }


@app.get("/alerts")
def alerts():
    query = """
    SELECT COUNT(*) AS alerts
    FROM inventory
    WHERE stock_level < 20
    """

    df = pd.read_sql(query, engine)

    return {
        "alerts": int(df["alerts"][0])
    }


@app.get("/top-products")
def top_products():
    query = """
    SELECT p.product_type, SUM(s.units_sold) as total_sales
    FROM sales_fact s
    JOIN products p ON s.sku = p.sku
    GROUP BY p.product_type
    ORDER BY total_sales DESC
    LIMIT 5
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")


@app.get("/supplier-defects")
def supplier_defects():
    query = """
    SELECT supplier_name, defect_rate
    FROM suppliers
    ORDER BY defect_rate DESC
    LIMIT 5
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")
@app.get("/supplier-defects")
def supplier_defects():

    query = """
    SELECT supplier_name, AVG(defect_rate) as defect_rate
    FROM suppliers
    GROUP BY supplier_name
    ORDER BY defect_rate DESC
    LIMIT 5
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")
@app.get("/logistics-cost")
def logistics_cost():

    query = """
    SELECT transportation_mode, AVG(shipping_cost) as avg_cost
    FROM logistics
    GROUP BY transportation_mode
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")
@app.get("/low-stock")
def low_stock():

    query = """
    SELECT sku, stock_level
    FROM inventory
    ORDER BY stock_level ASC
    LIMIT 5
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")