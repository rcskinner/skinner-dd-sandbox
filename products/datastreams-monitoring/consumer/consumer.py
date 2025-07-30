from kafka import KafkaConsumer
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "test-topic")
GROUP_ID = os.getenv("KAFKA_CONSUMER_GROUP", "test-group")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    group_id=GROUP_ID,
    enable_auto_commit=True
)

for message in consumer:
    print(f"Consumed: {message.value.decode('utf-8')}")