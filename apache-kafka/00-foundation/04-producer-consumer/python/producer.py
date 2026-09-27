from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092"
)

producer.send(
    "demo-topic",
    b"Hello Kafka "
)

producer.flush()
producer.close()

print(" Message sent ")
