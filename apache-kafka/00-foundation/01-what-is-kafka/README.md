# Topic #1 — What Is Apache Kafka?

> **Goal:** Understand what Apache Kafka is, why it exists, how its basic architecture works, and build a working Producer → Kafka → Consumer pipeline locally.

---

## 1. Learning Objectives

By the end of this chapter, you should be able to:

* Explain Apache Kafka in simple and technical terms.
* Understand why event streaming is useful.
* Explain the difference between synchronous APIs and event-driven communication.
* Understand producers, consumers, brokers, topics, partitions, records, and offsets.
* Explain why Kafka is distributed and scalable.
* Run Kafka locally with Docker.
* Publish a record using Python.
* Consume a record using Python.
* Inspect the topic, partition, and offset of a record.
* Explain Kafka's basic architecture in an interview.

---

# 2. What Is Apache Kafka?

**Apache Kafka is a distributed event streaming platform used to publish, store, process, and consume streams of events in a scalable, durable, and fault-tolerant way.**

A simpler way to think about Kafka:

> **Kafka is a distributed event log that allows applications to reliably exchange and process streams of data.**

For example, when a customer places an order:

```text
Customer
   │
   ▼
Order Service
   │
   │ OrderCreated
   ▼
 Kafka
   │
   ├───────────────┬────────────────┐
   ▼               ▼                ▼
Payment        Inventory       Notification
Service         Service           Service
```

The Order Service does not need to directly coordinate every downstream service.

It can publish an `OrderCreated` event to Kafka.

Other services can consume that event independently.

---

# 3. Why Do We Need Kafka?

Consider a traditional microservice architecture.

```text
                    ┌───► Payment Service
                    │
Order Service ──────┼───► Inventory Service
                    │
                    ├───► Notification Service
                    │
                    └───► Analytics Service
```

This can work, but as the system grows, several problems appear.

## 3.1 Tight Coupling

The Order Service needs to know about multiple downstream services.

If another service is introduced:

```text
Recommendation Service
```

the Order Service may need additional integration logic.

Over time, this can create a highly connected system.

---

## 3.2 Downstream Failures

Suppose:

```text
Order Service
      │
      ▼
Payment Service
      ✕
   unavailable
```

The Order Service now has to deal with the failure.

This can lead to:

* retries
* timeouts
* cascading failures
* complicated error handling
* increased request latency

Kafka can provide a buffer between the producer and consumers.

```text
Order Service
      │
      ▼
    Kafka
      │
      ▼
Payment Service
```

The producer can publish the event even when the consumer is temporarily unavailable, assuming Kafka is available and the producer's delivery requirements are satisfied.

The consumer can process the event when it becomes available again.

---

## 3.3 Traffic Spikes

Imagine an application normally receives:

```text
100 orders/second
```

During a large sale:

```text
50,000 orders/second
```

If every downstream service must immediately process every request synchronously, the entire system can become overloaded.

Kafka can act as a durable buffer:

```text
                     Traffic Spike
                          │
                          ▼
                    ┌───────────┐
                    │   Kafka   │
                    │   Topic   │
                    └─────┬─────┘
                          │
                    Consumers process
                    records at their
                    own capacity
```

Partitions also allow consumers to process records in parallel.

---

## 3.4 Temporary Service Unavailability

Suppose Notification Service is temporarily down.

Without an event log:

```text
Order → Notification Service ✕
```

With Kafka:

```text
Order Service
     │
     ▼
   Kafka
     │
     │ event retained
     ▼
Notification Service
     │
     └── processes it after recovery
```

The exact behavior depends on producer delivery settings, Kafka durability configuration, retention, and consumer processing.

---

# 4. Kafka Is More Than a Message Queue

Calling Kafka a **message queue** is not completely wrong, but it is incomplete.

Kafka's fundamental abstraction is a:

> **Distributed, durable, append-only log of records.**

Consider a Kafka partition:

```text
Partition 0

┌────┬────┬────┬────┬────┐
│ E0 │ E1 │ E2 │ E3 │ E4 │
└────┴────┴────┴────┴────┘
  0    1    2    3    4
       offsets
```

A consumer reading `E1` does not cause Kafka to immediately delete `E1`.

The record remains available according to the topic's retention policy.

This is one of the important differences between Kafka's log-based model and many traditional queueing systems.

---

# 5. What Is an Event?

An **event is a record of something that happened.**

Examples:

```text
UserRegistered
OrderCreated
PaymentCompleted
ShipmentDispatched
OrderCancelled
```

The event describes a fact that has already occurred.

For example:

```json
{
  "event_type": "OrderCreated",
  "order_id": 5001,
  "user_id": 101,
  "amount": 1499
}
```

This means:

> Order `5001` was created by user `101` for an amount of `1499`.

---

# 6. Message vs Event

The terms are often used interchangeably, but there is a useful distinction.

### Message

A message is data exchanged between systems.

```json
{
  "user_id": 101,
  "name": "Ashish"
}
```

### Event

An event communicates that something happened.

```json
{
  "event_type": "UserRegistered",
  "user_id": 101
}
```

In Kafka, we commonly work with **records**, which contain a key, value, timestamp, headers, and other metadata.

---

# 7. Kafka's Basic Architecture

The most important mental model is:

```text
                     Kafka Cluster
                          │
             ┌────────────┼────────────┐
             │            │            │
          Broker 1     Broker 2     Broker 3
             │            │            │
             └────────────┼────────────┘
                          │
                        Topic
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        Partition 0  Partition 1  Partition 2
             │            │            │
             ▼            ▼            ▼
          Records      Records      Records
             │            │            │
          Offsets      Offsets      Offsets
                          │
                          ▼
                       Consumers
```

The core concepts are:

```text
Cluster
  ↓
Broker
  ↓
Topic
  ↓
Partition
  ↓
Record
  ↓
Offset
  ↓
Consumer
  ↓
Consumer Group
```

Do not worry if these terms are not fully clear yet.

Each one will be covered in detail in later chapters.

---

# 8. Kafka Cluster

A **Kafka cluster** is a group of Kafka brokers working together.

For example:

```text
Kafka Cluster

┌──────────────┐
│   Broker 1   │
└──────────────┘

┌──────────────┐
│   Broker 2   │
└──────────────┘

┌──────────────┐
│   Broker 3   │
└──────────────┘
```

Multiple brokers allow Kafka to distribute data and workload across machines.

This provides the foundation for:

* scalability
* partition distribution
* replication
* fault tolerance
* parallel processing

---

# 9. Broker

A **broker** is a Kafka server.

A cluster can contain multiple brokers:

```text
Cluster
│
├── Broker 1
├── Broker 2
└── Broker 3
```

Brokers handle operations such as:

* accepting records from producers
* serving records to consumers
* storing partitions
* participating in replication
* handling cluster-related operations

---

# 10. Topic

A **topic** is a named stream/category to which records are published.

Examples:

```text
orders
payments
users
notifications
logs
```

For example:

```text
Topic: orders

OrderCreated
OrderCreated
OrderCancelled
OrderCreated
OrderDelivered
```

A topic is a logical abstraction.

Its data is actually distributed across one or more partitions.

```text
orders
  │
  ├── Partition 0
  ├── Partition 1
  └── Partition 2
```

---

# 11. Partition

A **partition is an ordered, append-only log within a Kafka topic.**

Example:

```text
Topic: orders

Partition 0
┌────┬────┬────┬────┐
│ E0 │ E1 │ E2 │ E3 │
└────┴────┴────┴────┘

Partition 1
┌────┬────┬────┐
│ E0 │ E1 │ E2 │
└────┴────┴────┘

Partition 2
┌────┬────┬────┬────┬────┐
│ E0 │ E1 │ E2 │ E3 │ E4 │
└────┴────┴────┴────┴────┘
```

Partitions are extremely important because they provide:

* scalability
* parallelism
* distribution
* ordering within a partition

### Important rule

Kafka guarantees ordering **within a partition**, not across an entire multi-partition topic.

For example:

```text
Partition 0:
A → B → C

Partition 1:
X → Y → Z
```

Kafka does not provide one global ordering between:

```text
A, B, C, X, Y, Z
```

This becomes especially important when designing partition keys.

We will study that later.

---

# 12. Record

A **record** is the basic unit of data written to Kafka.

A record can contain:

```text
Key
Value
Timestamp
Headers
Partition
Offset
```

Conceptually:

```text
┌─────────────────────────────┐
│ Key       = order-5001      │
│ Value     = OrderCreated    │
│ Timestamp = ...             │
│ Partition = 0               │
│ Offset    = 17              │
└─────────────────────────────┘
```

The producer creates the record.

Kafka stores it.

The consumer reads it.

---

# 13. Offset

An **offset is the sequential position of a record within a Kafka partition.**

Example:

```text
Partition 0

Offset    Record
  0       Order A
  1       Order B
  2       Order C
  3       Order D
  4       Order E
```

Therefore:

```text
Order C → offset 2
```

### Important

Offsets are **partition-specific**.

They are not globally unique.

For example:

```text
Partition 0 → offset 10
Partition 1 → offset 10
Partition 2 → offset 10
```

These can represent three different records.

A record's location is therefore commonly identified using:

```text
(topic, partition, offset)
```

---

# 14. Producer

A **producer** is an application that publishes records to Kafka.

```text
Order Service
      │
      ▼
   Producer
      │
      ▼
    Kafka
```

Python example:

```python
from kafka import KafkaProducer


def main() -> None:
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092"
    )

    producer.send(
        "demo-topic",
        b"Hello Kafka"
    )

    producer.flush()
    producer.close()

    print("Message sent successfully.")


if __name__ == "__main__":
    main()
```

The important operation is:

```python
producer.send("demo-topic", b"Hello Kafka")
```

This publishes a record to the `demo-topic` topic.

---

# 15. Consumer

A **consumer** is an application that reads records from Kafka.

```text
Kafka
  │
  ▼
Consumer
  │
  ▼
Payment Service
```

Python example:

```python
from kafka import KafkaConsumer


def main() -> None:
    consumer = KafkaConsumer(
        "demo-topic",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        group_id="demo-consumer-group",
    )

    print("Waiting for messages...")

    for message in consumer:
        print(
            f"topic={message.topic} "
            f"partition={message.partition} "
            f"offset={message.offset} "
            f"value={message.value.decode()}"
        )


if __name__ == "__main__":
    main()
```

Example output:

```text
Waiting for messages...
topic=demo-topic partition=0 offset=0 value=Hello Kafka
```

Notice the important metadata:

```text
topic
partition
offset
value
```

---

# 16. Producer → Kafka → Consumer

The basic Kafka flow is:

```text
┌──────────────┐
│   Producer   │
└──────┬───────┘
       │
       │ publish record
       ▼
┌──────────────────┐
│      Kafka       │
│                  │
│  demo-topic      │
│       │          │
│   Partition 0    │
└────────┬─────────┘
         │
         │ consume record
         ▼
┌──────────────────┐
│     Consumer     │
└──────────────────┘
```

In a microservices system:

```text
Order Service
      │
      │ OrderCreated
      ▼
    Kafka
      │
      ├────► Payment Service
      ├────► Inventory Service
      └────► Notification Service
```

---

# 17. Why Kafka Enables Asynchronous Communication

Consider:

```text
Order Service → Payment Service
```

The Order Service may need to wait for the Payment Service to respond.

With Kafka:

```text
Order Service
      │
      │ publish OrderCreated
      ▼
    Kafka
      │
      ▼
Payment Service
```

The producer and consumer are separated in time.

The consumer can process the event after it has been written to Kafka.

This is one of the key ideas behind event-driven architecture.

---

# 18. Kafka and Event Replay

One of Kafka's important capabilities is that records can remain available after a consumer has read them.

Example:

```text
Topic: orders

Offset
  0 → Order 1
  1 → Order 2
  2 → Order 3
  3 → Order 4
```

Suppose an Analytics Service processes the events.

Later, the Analytics Service needs to rebuild its state.

If the records are still within the topic's retention period, the service can consume the historical records again.

```text
Kafka
 │
 ├── Order 1
 ├── Order 2
 ├── Order 3
 └── Order 4
       │
       ▼
  Analytics Service
       │
       └── replay historical events
```

This is called **event replay**.

---

# 19. Consumer Groups — First Look

Suppose we have three instances of a Payment Service:

```text
Payment-1
Payment-2
Payment-3
```

They can belong to the same consumer group:

```text
payment-service
```

If the topic has three partitions:

```text
orders

Partition 0 ───► Payment-1
Partition 1 ───► Payment-2
Partition 2 ───► Payment-3
```

This allows records from different partitions to be processed in parallel.

There is an important relationship:

```text
Partitions → Parallelism within a consumer group
```

Consumer groups will be covered deeply in the next core-concepts chapters.

---

# 20. Real-World Example: Food Delivery

Imagine a food-delivery platform.

A customer places an order:

```text
Order #5001
```

The Order Service publishes:

```json
{
  "event_type": "OrderCreated",
  "order_id": 5001,
  "restaurant_id": 88,
  "user_id": 101,
  "amount": 649
}
```

Kafka receives the record:

```text
                  Order Service
                       │
                       │ OrderCreated
                       ▼
                ┌──────────────┐
                │    Kafka     │
                │ orders topic │
                └───────┬──────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
         Payment    Restaurant  Notification
          Service     Service      Service
```

Different consumers can react to the same business event independently.

For example:

```text
Payment Service
→ processes payment

Restaurant Service
→ updates restaurant order state

Notification Service
→ sends customer notification

Analytics Service
→ records business analytics
```

This is the core idea of event-driven architecture.

---

# 21. Kafka's Key Characteristics

## Distributed

Kafka can distribute partitions across multiple brokers.

## Durable

Records can be persisted to disk and replicated across brokers.

## Scalable

Topics can be divided into partitions, allowing work and storage to be distributed.

## Fault Tolerant

Replication allows Kafka to continue operating despite certain broker failures.

## High Throughput

Kafka is designed for high-volume data streams using mechanisms such as batching, sequential writes, and partitioning.

## Replayable

Consumers can process retained records again.

## Decoupled

Producers and consumers can evolve and scale independently.

---

# 22. Kafka vs Traditional Request/Response

### Traditional API

```text
Client
  │
  │ HTTP request
  ▼
Server
  │
  │ response
  ▼
Client
```

The communication is generally request/response oriented.

### Kafka

```text
Producer
    │
    │ event
    ▼
 Kafka
    │
    ├────► Consumer A
    ├────► Consumer B
    └────► Consumer C
```

Kafka is designed around event streams and asynchronous consumption.

This does not mean Kafka replaces REST or other APIs.

They solve different problems.

A real system commonly uses both:

```text
Frontend
   │
   │ HTTP
   ▼
Backend API
   │
   │ publish event
   ▼
 Kafka
   │
   ├──► Service A
   ├──► Service B
   └──► Service C
```

---

# 23. Kafka Is Not a Database

Kafka provides durable storage for event streams, but it is not a general-purpose relational database.

A relational database is designed around concepts such as:

```text
tables
rows
columns
relationships
indexes
transactions
queries
```

Kafka is primarily designed around:

```text
topics
partitions
records
offsets
event streams
consumer groups
```

You can use Kafka alongside a database:

```text
Application
    │
    ├──────────────► PostgreSQL
    │
    └──────────────► Kafka
```

Each system performs a different role.

---

# 24. Kafka Is Not Simply a Queue

A traditional queue often follows the conceptual model:

```text
Producer
   │
   ▼
Queue
   │
   ▼
Consumer
   │
   ▼
Message removed
```

Kafka uses a log-based model:

```text
Producer
   │
   ▼
Kafka Log
   │
   ├── Consumer A
   ├── Consumer B
   └── Consumer C
```

Records remain available according to retention policies.

Different consumer groups can independently process the same stream.

---

# 25. The Core Mental Model

If you remember only one diagram from this chapter, remember this:

```text
                    KAFKA CLUSTER
                         │
                ┌────────┼────────┐
                │        │        │
             Broker    Broker    Broker
                │
              Topic
                │
        ┌───────┼───────┐
        ▼       ▼       ▼
       P0      P1      P2
        │       │       │
        ▼       ▼       ▼
     Records Records Records
        │       │       │
        └───────┼───────┘
                │
             Consumers
                │
         Consumer Groups
```

And the application-level flow:

```text
Application
     │
     ▼
 Producer
     │
     ▼
   Topic
     │
     ▼
Partitions
     │
     ▼
 Kafka Brokers
     │
     ▼
Consumer Group
     │
     ▼
 Consumers
```

---

# 26. Hands-On Lab

Now let's actually run Kafka.

The objective is simple:

```text
Python Producer
      │
      ▼
     Kafka
      │
      ▼
Python Consumer
```

## Prerequisites

Check Docker:

```bash
docker --version
docker compose version
```

Check Python:

```bash
python3 --version
```

---

# 27. Project Files

This chapter contains:

```text
01-what-is-kafka/
│
├── README.md
├── producer.py
├── consumer.py
└── requirements.txt
```

`requirements.txt`:

```text
kafka-python
```

Create a virtual environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r 00-foundation/01-what-is-kafka/requirements.txt
```

---

# 28. Start Kafka

Kafka will run locally through Docker.

From the repository root:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Kafka should be running.

You can inspect the container logs with:

```bash
docker compose logs kafka
```

If your Compose service uses a different name, use the service name defined in `docker-compose.yml`.

---

# 29. Create the Producer

Create:

```text
00-foundation/01-what-is-kafka/producer.py
```

```python
from kafka import KafkaProducer


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "demo-topic"


def main() -> None:
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS
    )

    producer.send(
        TOPIC,
        b"Hello Kafka"
    )

    producer.flush()
    producer.close()

    print("Message sent successfully.")


if __name__ == "__main__":
    main()
```

Run:

```bash
python 00-foundation/01-what-is-kafka/producer.py
```

Expected:

```text
Message sent successfully.
```

---

# 30. Create the Consumer

Create:

```text
00-foundation/01-what-is-kafka/consumer.py
```

```python
from kafka import KafkaConsumer


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "demo-topic"
GROUP_ID = "demo-consumer-group"


def main() -> None:
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id=GROUP_ID,
    )

    print("Waiting for messages...")

    for message in consumer:
        value = message.value.decode("utf-8")

        print(
            f"topic={message.topic} "
            f"partition={message.partition} "
            f"offset={message.offset} "
            f"value={value}"
        )


if __name__ == "__main__":
    main()
```

Run:

```bash
python 00-foundation/01-what-is-kafka/consumer.py
```

Expected:

```text
Waiting for messages...
topic=demo-topic partition=0 offset=0 value=Hello Kafka
```

---

# 31. What Just Happened?

You just built your first Kafka pipeline.

```text
producer.py
     │
     │ "Hello Kafka"
     ▼
 Kafka Broker
     │
     ▼
demo-topic
     │
     ▼
Partition 0
     │
     │ offset 0
     ▼
consumer.py
```

The producer created a record.

Kafka stored the record in a topic partition.

The consumer fetched the record.

The consumer received metadata including:

```text
topic
partition
offset
value
```

That is the basic Kafka workflow.

---

# 32. Verify the Topic

You can inspect Kafka using the Kafka command-line tools provided by the container.

For example, depending on your Kafka image:

```bash
docker compose exec kafka \
  kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --list
```

You should see:

```text
demo-topic
```

You can inspect the topic:

```bash
docker compose exec kafka \
  kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic demo-topic
```

This gives you information about:

```text
topic
partition count
replication factor
partition leaders
```

The exact output depends on the Kafka version and Docker image being used.

---

# 33. Experiment: Send Multiple Events

Modify the producer:

```python
from kafka import KafkaProducer


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "demo-topic"


def main() -> None:
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS
    )

    messages = [
        b"Order 1001 created",
        b"Order 1002 created",
        b"Order 1003 created",
        b"Order 1004 created",
    ]

    for message in messages:
        producer.send(TOPIC, message)

    producer.flush()
    producer.close()

    print("All messages sent.")


if __name__ == "__main__":
    main()
```

Run:

```bash
python 00-foundation/01-what-is-kafka/producer.py
```

Then run the consumer.

You should observe different offsets:

```text
partition=0 offset=0 value=Order 1001 created
partition=0 offset=1 value=Order 1002 created
partition=0 offset=2 value=Order 1003 created
partition=0 offset=3 value=Order 1004 created
```

Now you can see the concept of an ordered log directly.

---

# 34. What You Should Understand Before Moving On

Do not move to advanced Kafka topics until these concepts are clear:

| Concept        | Meaning                                     |
| -------------- | ------------------------------------------- |
| Kafka          | Distributed event streaming platform        |
| Cluster        | Collection of Kafka brokers                 |
| Broker         | Kafka server                                |
| Topic          | Named stream/category of records            |
| Partition      | Ordered append-only log inside a topic      |
| Record         | Data stored in Kafka                        |
| Offset         | Position of a record within a partition     |
| Producer       | Publishes records                           |
| Consumer       | Reads records                               |
| Consumer Group | Group of consumers coordinating consumption |
| Retention      | How long records remain available           |
| Replay         | Reading retained historical records again   |

---

# 35. Quick Revision

### What is Kafka?

A distributed event streaming platform based around durable, partitioned logs.

### Why use Kafka?

Common reasons include:

```text
High-volume streaming
Asynchronous communication
Service decoupling
Scalability
Durability
Fault tolerance
Event replay
Real-time pipelines
```

### What is a topic?

A named stream/category of records.

### What is a partition?

An ordered log within a topic and a fundamental unit of Kafka's scalability and parallelism.

### What is an offset?

The sequential position of a record within a partition.

### What is a producer?

An application that publishes records.

### What is a consumer?

An application that reads records.

### What is a broker?

A Kafka server that stores and serves partitions.

### What is a consumer group?

A group of consumers that coordinate to consume partitions of a topic.

---

# 36. Interview Questions

### Beginner

1. What is Apache Kafka?
2. Why was Kafka created?
3. What is an event?
4. What is a Kafka topic?
5. What is a partition?
6. What is an offset?
7. What is a broker?
8. What is a producer?
9. What is a consumer?
10. What is a consumer group?

### Architecture

11. Why does Kafka use partitions?
12. Why is Kafka distributed?
13. Does Kafka guarantee ordering?
14. Is ordering guaranteed across partitions?
15. Why doesn't Kafka immediately delete a record after consumption?
16. What is event replay?
17. How does Kafka differ from a traditional message queue?
18. How does Kafka differ from REST APIs?
19. Is Kafka a database?
20. Why is Kafka useful in microservices?

---

# 37. Interview Answer

If an interviewer asks:

> **What is Apache Kafka?**

A strong answer is:

> Apache Kafka is a distributed event streaming platform designed to publish, store, and consume streams of records reliably at scale. Kafka organizes records into topics, topics are divided into partitions, and partitions are distributed across brokers. Producers publish records, while consumers read them through consumer groups. Because records are retained rather than immediately removed after consumption, Kafka can also support use cases such as event replay and real-time data pipelines.

### Short version

> **Kafka is a distributed event streaming platform built around durable, partitioned logs.**

---

# 38. Key Takeaway

The most important thing from this chapter is not memorizing definitions.

Understand this flow:

```text
                    PRODUCER
                       │
                       │ record
                       ▼
                ┌──────────────┐
                │    KAFKA     │
                │              │
                │    TOPIC     │
                │      │       │
                │ ┌────┼────┐  │
                │ ▼    ▼    ▼  │
                │ P0   P1   P2  │
                └─┬────┬────┬──┘
                  │    │    │
                  └────┼────┘
                       ▼
                 CONSUMER GROUP
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
          Consumer  Consumer  Consumer
```

Once this model is clear, the rest of Kafka becomes much easier to understand.

---

## Next Topic

**Topic #2 — Kafka Broker**

We will go deeper into:

```text
What exactly is a broker?
How does a broker store data?
How does a producer find a broker?
What is a bootstrap server?
How do brokers communicate?
What happens when a broker goes down?
How are partitions distributed?
What is a leader?
What is a follower?
What is replication?
What is ISR?
```

The next chapters will build on this foundation rather than repeating it.
