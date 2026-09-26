from kafka import KafkaConsumer
import json


KAFKA_BROKER = "localhost:9092"
TOPIC = "orders"
GROUP_ID = "order-service"


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id=GROUP_ID,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    ),
)


print("Consumer started")
print(f"Listening to topic: {TOPIC}")


try:
    for message in consumer:
        order = message.value

        print(
            f"Received message | "
            f"partition={message.partition} | "
            f"offset={message.offset}"
        )

        print("Order:", order)

except KeyboardInterrupt:
    print("Consumer stopped")

finally:
    consumer.close()