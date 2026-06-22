from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

print("Connecting to Kafka...")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Connected")

skus = [f"SKU{i}" for i in range(100)]

print("\nSending sales to Kafka. Press Ctrl+C to stop.\n")

try:
    count = 0

    while True:
        units = random.randint(1, 20)
        revenue = round(random.uniform(500, 5000), 2)

        sale = {
            "sku": random.choice(skus),
            "units_sold": units,
            "revenue_generated": revenue,
            "created_at": datetime.now().isoformat()
        }

        producer.send("sales_topic", sale)

        count += 1

        print(
            f"[{count}] Sent {sale['sku']} | Units={units} | Revenue=₹{revenue}"
        )

        time.sleep(3)

except KeyboardInterrupt:
    print("\nStopping producer")
    producer.close()