import json

from kafka import KafkaConsumer


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "orders"
GROUP_ID = "order-service"


def create_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),
    )


def main() -> None:
    consumer = create_consumer()

    print(f"Listening to topic: {TOPIC}")
    print(f"Consumer group: {GROUP_ID}")
    print("Press Ctrl+C to stop.\n")

    try:
        for message in consumer:
            print("Event received:")
            print(json.dumps(message.value, indent=2))

            print(f"Topic: {message.topic}")
            print(f"Partition: {message.partition}")
            print(f"Offset: {message.offset}")
            print("-" * 50)

    except KeyboardInterrupt:
        print("\nStopping consumer...")

    finally:
        consumer.close()


if __name__ == "__main__":
    main()