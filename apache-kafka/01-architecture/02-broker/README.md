
---

# 02-broker/README.md

```markdown
# Kafka Broker

A Kafka Broker is a Kafka server.

It receives records from producers and serves records to consumers.

A Kafka cluster normally contains multiple brokers.

---

## 1. What is a Broker?

A broker is a Kafka server that:

- Stores partition data
- Receives records from producers
- Serves records to consumers
- Handles partition replicas
- Participates in cluster operations

Example:

```text
Producer
    |
    v
+-----------+
|  Broker   |
+-----------+
    |
    v
Consumer