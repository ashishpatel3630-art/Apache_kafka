from kafka import KafkaConsumer
import json


TOPIC = "pubsub-orders"
GROUP_ID = "analytics-service"


def create_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers="localhost:9092",
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        client_id="analytics-consumer",
    )


def main() -> None:
    consumer = create_consumer()

    print("Analytics Service started")
    print(f"Consumer Group: {GROUP_ID}")
    print("Waiting for events...\n")

    try:
        for message in consumer:
            event = message.value

            print(
                f"[ANALYTICS] "
                f"Received order={event['order_id']} "
                f"amount={event['amount']} "
                f"partition={message.partition} "
                f"offset={message.offset}"
            )

    except KeyboardInterrupt:
        print("\nAnalytics Service stopped.")

    finally:
        consumer.close()


if __name__ == "__main__":
    main()