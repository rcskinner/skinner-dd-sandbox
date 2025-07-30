from kafka import KafkaProducer
import time
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "test-topic")

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

i = 0
while True:
    message = f"Message {i}"
    producer.send(TOPIC, message.encode("utf-8"))
    print(f"Produced: {message}")
    i += 1
    time.sleep(1)