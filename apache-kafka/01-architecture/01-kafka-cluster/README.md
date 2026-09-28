# Kafka Cluster

A Kafka Cluster is a group of Kafka brokers working together.

Instead of running Kafka on only one server, we can run multiple Kafka brokers.

This helps Kafka provide:

- Scalability
- Fault tolerance
- High availability
- Distributed data processing

---

## 1. What is a Kafka Cluster?

A Kafka Cluster is simply multiple Kafka brokers connected together.

Example:

```text
              Kafka Cluster
        +-----------------------+
        |                       |
        |  +--------+           |
        |  |Broker 1|           |
        |  +--------+           |
        |                       |
        |  +--------+           |
        |  |Broker 2|           |
        |  +--------+           |
        |                       |
        |  +--------+           |
        |  |Broker 3|           |
        |  +--------+           |
        |                       |
        +-----------------------+