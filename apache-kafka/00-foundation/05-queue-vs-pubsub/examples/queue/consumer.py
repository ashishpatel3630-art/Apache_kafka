"""
Kafka Queue Pattern - Consumer

Run this file from multiple terminals.

All consumers use the same consumer group:

    order-workers

Kafka will distribute partitions among them.

Requirements:
    pip install kafka-python
"""

import json
from kafka import KafkaConsumer


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "orders"
GROUP_ID = "order-workers"


def create_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )


def main() -> None:
    consumer = create_consumer()

    print(f"Consumer started")
    print(f"Topic: {TOPIC}")
    print(f"Group: {GROUP_ID}")
    print("Waiting for orders...\n")

    try:
        for message in consumer:
            order = message.value

            print(
                f"[WORKER] "
                f"order_id={order['order_id']} "
                f"partition={message.partition} "
                f"offset={message.offset}"
            )

    finally:
        consumer.close()


if __name__ == "__main__":
    main()