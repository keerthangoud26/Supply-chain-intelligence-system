from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PostgreSQL connection (Neon Cloud)
engine = create_engine(
    "postgresql://neondb_owner:npg_dWfz6tks9Yvn@ep-autumn-breeze-athxybzz.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require"
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
    SELECT transportation_mode, AVG(shipping_cost) AS avg_cost
    FROM logistics
    GROUP BY transportation_mode
    """

    df = pd.read_sql(query, engine)

    # USD to INR conversion
    usd_to_inr = 95

    df["avg_cost"] = df["avg_cost"] * usd_to_inr

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
@app.get("/anomalies")
def anomalies():

    anomalies_list = []

    # Inventory anomaly
    inventory_query = """
    SELECT sku, stock_level
    FROM inventory
    WHERE stock_level < 5
    LIMIT 3
    """

    inventory_df = pd.read_sql(inventory_query, engine)

    for _, row in inventory_df.iterrows():
        anomalies_list.append({
            "type": "Inventory",
            "message": f"{row['sku']} critically low stock"
        })

    # Supplier anomaly
    supplier_query = """
    SELECT supplier_name, defect_rate
    FROM suppliers
    WHERE defect_rate > 4
    LIMIT 2
    """

    supplier_df = pd.read_sql(supplier_query, engine)

    for _, row in supplier_df.iterrows():
        anomalies_list.append({
            "type": "Supplier",
            "message": f"{row['supplier_name']} high defect rate"
        })

    return anomalies_list
@app.get("/activity-logs")
def activity_logs():

    logs = []

    # Low stock events
    stock_query = """
    SELECT sku, stock_level
    FROM inventory
    ORDER BY stock_level ASC
    LIMIT 3
    """

    stock_df = pd.read_sql(stock_query, engine)

    for _, row in stock_df.iterrows():
        logs.append({
            "message": f"Inventory alert: {row['sku']} stock dropped to {row['stock_level']}"
        })

    # Supplier quality events
    supplier_query = """
    SELECT supplier_name, defect_rate
    FROM suppliers
    ORDER BY defect_rate DESC
    LIMIT 2
    """

    supplier_df = pd.read_sql(supplier_query, engine)

    for _, row in supplier_df.iterrows():
        logs.append({
            "message": f"Supplier update: {row['supplier_name']} defect rate at {round(row['defect_rate'],2)}%"
        })

    # Logistics events
    logistics_query = """
    SELECT transportation_mode, shipping_cost
    FROM logistics
    ORDER BY shipping_cost DESC
    LIMIT 2
    """

    logistics_df = pd.read_sql(logistics_query, engine)

    for _, row in logistics_df.iterrows():
        logs.append({
            "message": f"Logistics update: {row['transportation_mode']} shipping cost ₹{round(row['shipping_cost'] * 95,2)}"
        })

    return logs
@app.get("/revenue-forecast")
def revenue_forecast():

    query = """
    SELECT revenue_generated
    FROM sales_fact
    ORDER BY sale_id
    """

    df = pd.read_sql(query, engine)

    # historical revenue
    y = df["revenue_generated"].values

    # create X = [0,1,2...]
    X = np.array(range(len(y))).reshape(-1, 1)

    # train model
    model = LinearRegression()
    model.fit(X, y)

    # predict next 7 future points
    future_X = np.array(range(len(y), len(y) + 7)).reshape(-1, 1)
    predictions = model.predict(future_X)

    result = []

    for i, pred in enumerate(predictions):
        result.append({
            "day": f"Day {i+1}",
            "prediction": round(float(pred), 2)
        })

    return result