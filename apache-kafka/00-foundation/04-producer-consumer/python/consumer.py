from kafka import KafkaConsumer

Consumer = KafkaConsumer(
    "demo-topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="demo_group"
)

print("waiting for messages ")

for message in Consumer:
 print(message.value.decode("utf-8"))