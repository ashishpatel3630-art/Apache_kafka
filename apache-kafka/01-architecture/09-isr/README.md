
---

# 09-isr/README.md

# Kafka ISR

ISR stands for:

> In-Sync Replicas

ISR is an important concept in Kafka replication.

It represents replicas that are sufficiently caught up with the leader.

---

## 1. What is ISR?

Suppose a partition has:

```text
Broker 1 → Leader
Broker 2 → Follower
Broker 3 → Follower