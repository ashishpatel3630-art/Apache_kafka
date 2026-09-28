# Kafka vs RabbitMQ

Kafka and RabbitMQ are both used to send messages between applications and services.

But they work in different ways.

The easiest way to remember:

- Kafka → Event Streaming
- RabbitMQ → Message Queue

---

## 1. What is Kafka?

Apache Kafka is a system used to send, store, and process events.

Example:

```text
Order Service
      |
      | Order Created
      v
    Kafka
      |
      +------> Payment Service
      |
      +------> Inventory Service
      |
      +------> Notification Service