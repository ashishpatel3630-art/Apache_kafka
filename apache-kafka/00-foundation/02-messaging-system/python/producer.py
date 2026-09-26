from kafka import KafkaProducer
import json
import time

KAFKA_BROKER = "localhost:9092"
TOPIC = "orders"

producer = KafkaProducer(
    bootstrap_servers = KAFKA_BROKER,
    value_serializer=lambda 
    value: json.dumps(value).encode("utf-8"),
    
)

def send_order(order_id: int ) -> None:
    order ={
        "order_id": order_id,
        "customer": f"customer-{order_id}",
        "amount": 1000 + order_id *100 ,
        "status":"created",
        
    }
    
    future = producer.send(
        TOPIC ,
        value=order,
    )
    metadata = future.get(timeout=10)
    print(
        f"message sent | "
        f"topic = {metadata.topic} | "
        f"partition={metadata.partition} |"
        f"offset = {metadata.offset}"
    )
if __name__ == "__main__":
    print("Producer started")

    for order_id in range(1, 6):
        send_order(order_id)
        time.sleep(1)

    producer.flush()
    producer.close()

    print("Producer stopped")