import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Load raw
df = pd.read_csv('supply_chain_data.csv')
print(f"Raw: {len(df)} rows")

# Generate proper date range (simulate daily sales)
np.random.seed(42)
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Create daily sales for top products
products = df['Product type'].unique()[:5]  # Take 5 products
data = []
for date in dates:
    for product in products:
        base = np.random.normal(100, 20)
        if date.weekday() >= 5:  # Weekend boost
            base *= 1.3
        if date.month in [11, 12]:  # Holiday boost
            base *= 1.5
        quantity = max(0, int(base + np.random.normal(0, 10)))
        price = np.random.uniform(50, 200)
        data.append([date, product, quantity, round(price, 2)])

clean_df = pd.DataFrame(data, columns=['order_date', 'product_name', 'quantity', 'price'])

# Load to PostgreSQL
engine = create_engine('postgresql://admin:admin123@localhost:5432/supplychain')
clean_df.to_sql('sales_daily', engine, if_exists='replace', index=False)

print(f"✅ Created daily sales: {len(clean_df)} rows")
print(f"Products: {clean_df['product_name'].unique().tolist()}")
print(f"Date range: {clean_df['order_date'].min()} to {clean_df['order_date'].max()}")