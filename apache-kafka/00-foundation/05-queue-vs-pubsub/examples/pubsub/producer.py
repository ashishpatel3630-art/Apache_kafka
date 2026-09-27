import json 
from kafka import KafkaProducer

import time

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "orders"

def create_producer()->KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda value:json.dumps(value).encode("utf-8"),
        
    )
    
def main()->None:
    producer = create_producer()
    
    try:
        for order_id in range(1,10):
            event = {
                "event":"order_created",
                "order_id":order_id,
                "customer":f"customer-{order_id}",
                "item":"pizza",
            }
            
            future = producer.send(TOPIC , value=event)
            metadata = future.get(timeout=10)
            
            print(
                f"Published order={order_id} "
                f"partition={metadata.partition} "
                f"offset={metadata.offset}"
            )
            
            time.sleep(1)
            
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    main()
    