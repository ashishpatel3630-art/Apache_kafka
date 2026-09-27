"""
Kafka Queue Pattern - Producer

Produces order messages to the `orders` topic.

Requirements:
    pip install kafka-python
"""

import json
from kafka import KafkaProducer


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "orders"


def create_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )


def main() -> None:
    producer = create_producer()

    try:
        for order_id in range(1, 11):
            order = {
                "event": "order_created",
                "order_id": order_id,
                "customer": f"customer-{order_id}",
                "item": "Pizza",
                "quantity": 1,
            }

            future = producer.send(TOPIC, value=order)

            metadata = future.get(timeout=10)

            print(
                f"Produced order={order_id} "
                f"partition={metadata.partition} "
                f"offset={metadata.offset}"
            )

    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()