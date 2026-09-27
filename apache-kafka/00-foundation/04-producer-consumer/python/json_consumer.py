import json

from kafka import KafkaConsumer

Consumer = KafkaConsumer(
    "demo-topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="order-service",
    value_deserializer=lambda value:json.loads(value.decode("utf-8"))
    
)

print("waiting for orders :")

for messages in Consumer:
    order = messages.value
    
print( 
    f"Order: {order['order_id']} |"
    f"Customer: {order['customer']} | "
    f"Amount: ₹{order['amount']}"
          
    )