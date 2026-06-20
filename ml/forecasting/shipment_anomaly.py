import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest

# Database connection
engine = create_engine(
    "postgresql://admin:admin123@localhost:5432/supplychain"
)

# Load shipment data
query = """
SELECT
    shipping_time,
    shipping_cost,
    transportation_mode,
    shipping_carrier
FROM logistics
"""

df = pd.read_sql(query, engine)

print("Data Loaded")
print(df.head())

# Encode categorical columns
cat_cols = [
    "transportation_mode",
    "shipping_carrier"
]

for col in cat_cols:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])

print("\nEncoded Data")
print(df.head())

# Train anomaly detection model
model = IsolationForest(
    contamination=0.1,
    random_state=42
)

# Fit model
df["anomaly"] = model.fit_predict(df)

# -1 = anomaly, 1 = normal
anomalies = df[df["anomaly"] == -1]

print("\n========== ANOMALIES DETECTED ==========")
print(anomalies)

print(f"\nTotal Anomalies Found: {len(anomalies)}")