
---

# 10-controller/README.md

```markdown
# Kafka Controller

The Kafka Controller is responsible for important cluster-level management tasks.

Modern Kafka uses KRaft, where controller responsibilities are handled by Kafka's metadata quorum.

---

## 1. What is the Controller?

The controller manages important cluster metadata and coordination tasks.

It can handle things such as:

- Broker membership changes
- Partition leadership
- Partition state
- Replica assignments
- Metadata changes

---

## 2. Controller in a Kafka Cluster

Example:

```text
              Kafka Cluster

        +-----------------------+
        |                       |
        |      Controller       |
        |           |           |
        |     +-----+-----+     |
        |     |           |     |
        |     v           v     |
        |  Broker 1    Broker 2 |
        |                       |
        |        Broker 3       |
        +-----------------------+