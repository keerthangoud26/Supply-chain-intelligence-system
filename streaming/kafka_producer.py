from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd

print("Connecting to Kafka...")
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
print("✅ Connected")

# Load products
engine = create_engine('postgresql://admin:admin123@localhost:5432/supplychain')
df = pd.read_sql("SELECT DISTINCT product_name FROM sales_daily", engine)
products = df['product_name'].tolist()
print(f"Products: {products}")

print("\n📤 Sending sales to Kafka. Press Ctrl+C to stop.\n")

try:
    count = 0
    while True:
        sale = {
            'timestamp': datetime.now().isoformat(),
            'product': random.choice(products),
            'quantity': random.randint(1, 20),
            'price': round(random.uniform(10, 200), 2),
            'location': random.choice(['Mumbai', 'Delhi', 'Bangalore'])
        }
        
        producer.send('sales_topic', sale)
        count += 1
        print(f"[{count}] ✅ {sale['product']} x{sale['quantity']} @ ₹{sale['price']}")
        time.sleep(2)
        
except KeyboardInterrupt:
    print(f"\n⏹️ Sent {count} messages. Stopping.")
    producer.close()    