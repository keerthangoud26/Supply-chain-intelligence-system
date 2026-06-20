import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import warnings
warnings.filterwarnings('ignore')

print("Loading data...")
engine = create_engine('postgresql://admin:admin123@localhost:5432/supplychain')
df = pd.read_sql("SELECT * FROM sales_daily ORDER BY order_date", engine)

# Aggregate all products (total daily demand)
daily_total = df.groupby('order_date')['quantity'].sum().reset_index()
daily_total.columns = ['ds', 'y']
daily_total['ds'] = pd.to_datetime(daily_total['ds'])

print(f"Total demand: {len(daily_total)} days")
print(f"Avg daily: {daily_total['y'].mean():.0f} units")

# Train/test split
train = daily_total[daily_total['ds'] < '2023-12-01']
test = daily_total[daily_total['ds'] >= '2023-12-01']

print(f"Train: {len(train)} days, Test: {len(test)} days")

# Train Prophet with more seasonality
print("Training Prophet...")
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.05
)
model.fit(train)

# Forecast
future = model.make_future_dataframe(periods=len(test))
forecast = model.predict(future)

# Evaluate
y_pred = forecast[forecast['ds'] >= '2023-12-01']['yhat']
mae = mean_absolute_error(test['y'], y_pred)
mape = mean_absolute_percentage_error(test['y'], y_pred)

print(f"\n✅ Prophet Results:")
print(f"   MAE: {mae:.2f} units")
print(f"   MAPE: {mape:.2%}")
print(f"   Baseline (mean): {test['y'].mean():.0f} units")

# Save
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_sql('forecast_results', engine, if_exists='replace', index=False)
print("✅ Done")