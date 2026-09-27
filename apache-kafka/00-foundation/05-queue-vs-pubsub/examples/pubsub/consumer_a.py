import json
import time 
from kafka import KafkaConsumer

BOOTSTRAP_SERVICES = "localhost:9092",
TOPIC = "orders",
GROUP_ID ="payment_service"

def create_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVICES,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer= lambda value: json.loads(value.decode("utf-8")),
    )
    
def main() -> None:
    consumer = create_consumer()
    
    print("Payment Service started")
    print(f"Consumer Group: {GROUP_ID}")
    print("Waiting for order events...\n")

    try:
        for message in consumer:
            event = message.value

            print(
                f"[PAYMENT] "
                f"Processing order={event['order_id']} "
                f"partition={message.partition} "
                f"offset={message.offset}"
            )

    finally:
        consumer.close()


if __name__ == "__main__":
    main()