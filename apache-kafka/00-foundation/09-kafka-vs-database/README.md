# Kafka vs Database

Kafka and Databases are both important technologies used in modern applications.

But they solve different problems.

The easiest way to remember:

Kafka
→ Events / Streams

Database
→ Data / Storage

---

# 1. What is Kafka?

Apache Kafka is an event streaming platform.

It is used to:

- Send events
- Store events for a period of time
- Process streams
- Connect different services
- Build event-driven systems
- Handle high-volume data

Example:

```text
Order Service
      |
      | OrderCreated
      v
    Kafka
      |
      +------> Payment Service
      |
      +------> Inventory Service
      |
      +------> Notification Service
      |
      +------> Analytics Service