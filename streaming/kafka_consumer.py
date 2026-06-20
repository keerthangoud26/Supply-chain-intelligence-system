from kafka import KafkaConsumer
import json
import psycopg2
from datetime import datetime
import time

print("🔄 Connecting to Kafka...")
consumer = KafkaConsumer(
    'sales_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
print("✅ Connected")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="supplychain",
    user="admin",
    password="admin123"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS realtime_sales (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        product VARCHAR(50),
        quantity INT,
        price FLOAT,
        location VARCHAR(50),
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
print("✅ PostgreSQL ready")

print("\n📥 Listening for sales. Press Ctrl+C to stop.\n")

count = 0
try:
    for message in consumer:
        data = message.value
        count += 1
        
        cur.execute("""
            INSERT INTO realtime_sales (timestamp, product, quantity, price, location)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['timestamp'], data['product'], data['quantity'], data['price'], data['location']))
        conn.commit()
        
        print(f"[{count}] ✅ Saved: {data['product']} x{data['quantity']}")
        
except KeyboardInterrupt:
    print(f"\n⏹️ Saved {count} records. Closing.")
finally:
    cur.close()
    conn.close()
    consumer.close()