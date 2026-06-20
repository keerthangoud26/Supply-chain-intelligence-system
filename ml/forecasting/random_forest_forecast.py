import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Load data
engine = create_engine('postgresql://admin:admin123@localhost:5432/supplychain')
df = pd.read_sql("SELECT * FROM sales_daily ORDER BY order_date", engine)
print(f"Loaded: {len(df)} rows")

# Feature engineering
df['day_of_week'] = pd.to_datetime(df['order_date']).dt.dayofweek
df['month'] = pd.to_datetime(df['order_date']).dt.month
df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
df['is_holiday'] = df['month'].apply(lambda x: 1 if x in [11, 12] else 0)

# Create lag features
for lag in [1, 7, 14, 30]:
    df[f'lag_{lag}'] = df.groupby('product_name')['quantity'].shift(lag)

# Drop nulls
df = df.dropna()

# Train on 80%, test on 20%
train = df[df['order_date'] < '2023-12-01']
test = df[df['order_date'] >= '2023-12-01']

features = ['day_of_week', 'month', 'is_weekend', 'is_holiday', 
            'lag_1', 'lag_7', 'lag_14', 'lag_30']

X_train = train[features]
y_train = train['quantity']
X_test = test[features]
y_test = test['quantity']

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Model performance:")
print(f"   MAE: {mae:.2f} units")
print(f"   R² Score: {r2:.3f}")
print(f"   Test size: {len(test)} rows")

# Feature importance
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(importance)