
# When to Use Kafka

Kafka is useful when applications need event-driven communication and event streaming.

---

# 1. Event-Driven Microservices

Example:

```text
Order Service
      |
      | OrderCreated
      v
    Kafka
      |
      +----> Payment
      +----> Inventory
      +----> Notification