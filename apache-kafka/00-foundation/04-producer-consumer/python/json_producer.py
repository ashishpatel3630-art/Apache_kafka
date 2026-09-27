import json 

from kafka import KafkaProducer

Producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value:json.dumps(value).encode("utf-8")   
)

order = {
    "order_id":"ORD-101",
    "customer":"ashish",
    "amount":"450"
}

Producer.send("demo-topic",order)

Producer.flush()
Producer.close()

print("order sent ")
