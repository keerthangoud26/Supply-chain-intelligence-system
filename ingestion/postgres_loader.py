import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv("data/raw/supply_chain_data.csv")

print("CSV Loaded Successfully")
print(f"Rows: {len(df)}")

# PostgreSQL connection
engine = create_engine(
    "postgresql://admin:admin123@localhost:5432/supplychain"
)

# ---------------- PRODUCTS ----------------
products = df[["SKU", "Product type", "Price"]].drop_duplicates()
products.columns = ["sku", "product_type", "price"]

products.to_sql(
    "products",
    engine,
    if_exists="append",
    index=False
)

print("Products Loaded")


# ---------------- SUPPLIERS ----------------
suppliers = df[
    [
        "Supplier name",
        "Location",
        "Lead time",
        "Defect rates",
        "Inspection results"
    ]
].drop_duplicates()

suppliers.columns = [
    "supplier_name",
    "location",
    "lead_time",
    "defect_rate",
    "inspection_result"
]

suppliers.to_sql(
    "suppliers",
    engine,
    if_exists="append",
    index=False
)

print("Suppliers Loaded")


# ---------------- INVENTORY ----------------
inventory = df[
    [
        "SKU",
        "Stock levels",
        "Availability",
        "Order quantities"
    ]
]

inventory.columns = [
    "sku",
    "stock_level",
    "availability",
    "order_quantity"
]

inventory.to_sql(
    "inventory",
    engine,
    if_exists="append",
    index=False
)

print("Inventory Loaded")


# ---------------- LOGISTICS ----------------
logistics = df[
    [
        "SKU",
        "Shipping carriers",
        "Shipping times",
        "Shipping costs",
        "Transportation modes",
        "Routes"
    ]
]

logistics.columns = [
    "sku",
    "shipping_carrier",
    "shipping_time",
    "shipping_cost",
    "transportation_mode",
    "route"
]

logistics.to_sql(
    "logistics",
    engine,
    if_exists="append",
    index=False
)

print("Logistics Loaded")


# ---------------- MANUFACTURING ----------------
manufacturing = df[
    [
        "SKU",
        "Production volumes",
        "Manufacturing lead time",
        "Manufacturing costs"
    ]
]

manufacturing.columns = [
    "sku",
    "production_volume",
    "manufacturing_lead_time",
    "manufacturing_cost"
]

manufacturing.to_sql(
    "manufacturing",
    engine,
    if_exists="append",
    index=False
)

print("Manufacturing Loaded")


# ---------------- SALES FACT ----------------
sales = df[
    [
        "SKU",
        "Number of products sold",
        "Revenue generated"
    ]
]

sales.columns = [
    "sku",
    "units_sold",
    "revenue_generated"
]

sales.to_sql(
    "sales_fact",
    engine,
    if_exists="append",
    index=False
)

print("Sales Fact Loaded")

print("ETL Completed Successfully")