
---

# 07-leader-follower/README.md

```markdown
# Kafka Leader and Follower

Kafka uses replicas to provide fault tolerance.

For a partition, one replica acts as the leader and other replicas act as followers.

---

## 1. What is a Replica?

A replica is a copy of a partition.

Example:

```text
Partition 0

Broker 1 → Replica
Broker 2 → Replica
Broker 3 → Replica