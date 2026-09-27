#  Producer & Consumer

A kafka Producer sends request to Kafka 
A Kafka Consumer Reads Records from kafka

Producer 
    |
    |
Kafka Topic 
    |
    |
Consumer

# 1. Producer

A Producer is an application that publishes records to a Kafka topic.

# 2. Consumer

A Consumer is an application that reads records from a Kafka topic.

# 3. Producer → Kafka → Consumer

             Kafka
        ┌─────────────────┐
        │   orders topic  │
        │                 │
Producer│  P0  P1  P2     │Consumer
   ────►│                 │────►
        └─────────────────┘

The Producer does not directly communicate with the Consumer.

Kafka acts as the middle layer.

# 4. Setup

Install the Python Kafka client:

pip install -r python/requirements.txt

Kafka should be running on:

localhost:9092
# 5. Create Topic
bash commands/kafka-commands.sh

Or manually:

kafka-topics.sh \
  --create \
  --topic demo-topic \
  --bootstrap-server localhost:9092

Check topics:

kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092
# 6. Run Producer
python python/producer.py

Expected:

Message sent!
# 7. Run Consumer

Open another terminal:

python python/consumer.py

Expected:

Waiting for messages...
Hello Kafka

# 8. Consumer group 

Multiple consumers can belong to the same consumer group.

            orders
                │
       ┌────────┴────────┐
       ▼                 ▼
   Consumer 1         Consumer 2
       │                 │
       └──── group ──────┘

Kafka distributes partitions between consumers in the same group.

Different consumer groups receive their own copy of the records.

    orders topic
          │
      ┌───┴─────────────┐
      ▼                 ▼
payment-group   notification-group

