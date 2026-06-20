import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# PostgreSQL connection
engine = create_engine(
    "postgresql://admin:admin123@localhost:5432/supplychain"
)

# Load logistics + product data
query = """
SELECT
    l.shipping_time,
    l.shipping_cost,
    l.transportation_mode,
    l.route,
    l.shipping_carrier,
    p.price,
    p.product_type,
    m.manufacturing_cost,
    m.manufacturing_lead_time
FROM logistics l
JOIN products p
ON l.sku = p.sku
JOIN manufacturing m
ON l.sku = m.sku
"""

df = pd.read_sql(query, engine)

print("Data Loaded Successfully")
print(df.head())
print(f"Total Rows: {len(df)}")

# Encode categorical columns
from sklearn.preprocessing import LabelEncoder

cat_columns = [
    "transportation_mode",
    "route",
    "shipping_carrier",
    "product_type"
]

for col in cat_columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])



# Features and target
X = df[
    [
        "shipping_time",
        "transportation_mode",
        "route",
        "shipping_carrier",
        "price",
        "product_type",
        "manufacturing_cost",
        "manufacturing_lead_time"
    ]
]

y = df["shipping_cost"]

print("\nFeatures Created")
print(X.head())

print("\nTarget Variable")
print(y.head())

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTrain Test Split Completed")
print(f"Training Rows: {len(X_train)}")
print(f"Testing Rows: {len(X_test)}")

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("\nModel Training Completed")

# Make predictions
y_pred = model.predict(X_test)

print("\nPredictions Generated")
print(y_pred[:5])

# Evaluate model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n========== MODEL PERFORMANCE ==========")
print(f"MAE: {mae:.3f}")
print(f"R2 Score: {r2:.3f}")

# Feature importance
importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print("\n========== FEATURE IMPORTANCE ==========")
print(importance)