from kafka import KafkaConsumer
import json
import psycopg2

print("Connecting to Kafka...")

consumer = KafkaConsumer(
    "sales_topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Connected")

conn = psycopg2.connect(
    host="localhost",
    database="supplychain",
    user="admin",
    password="admin123"
)

cur = conn.cursor()

print("\nListening for sales...\n")

count = 0

try:
    for message in consumer:

        data = message.value
        count += 1

        cur.execute(
            """
            INSERT INTO sales_fact
            (sku, units_sold, revenue_generated, created_at)
            VALUES (%s, %s, %s, %s)
            """,
            (
                data["sku"],
                data["units_sold"],
                data["revenue_generated"],
                data["created_at"]
            )
        )

        conn.commit()

        print(
            f"[{count}] Saved {data['sku']} Revenue ₹{data['revenue_generated']}"
        )

except KeyboardInterrupt:
    print("\nStopping consumer")

finally:
    cur.close()
    conn.close()
    consumer.close()