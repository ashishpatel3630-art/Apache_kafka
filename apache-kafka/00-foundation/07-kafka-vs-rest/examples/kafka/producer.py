import json
from kafka import KafkaProducer

BOOTSTRAP_SERVER = "localhost:9092" 
TOPIC : "orders"

def create_producer()-> KafkaProducer():
    return KafkaProducer(
        bootstrap_servers= BOOTSTRAP_SERVER,
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )
    
def main()->None:
    producer = create_producer()
    
    event = {
        "event": "OrderCreated",
        "order_id": 101,
        "customer": "Ashish",
        "product": "MacBook",
        "quantity": 1,
        
    }
    
    try:
        
        future = producer.send(TOPIC , value=event)
        
        metadata = future.get(timeout=10)
        
        print("Event published successfully.")
        print(f"Topic: {metadata.topic}")
        print(f"Partition: {metadata.partition}")
        print(f"Offset: {metadata.offset}")
        
    except Exception as error :
        print(f"failed to publish event : {error}")
        
    finally:
        producer.flush()
        producer.close()
        
if __name__ == "__main__":
    main()
        