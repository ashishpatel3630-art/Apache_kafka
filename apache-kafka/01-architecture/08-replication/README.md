
---

# 08-replication/README.md

```markdown
# Kafka Replication

Replication means keeping copies of partition data on multiple Kafka brokers.

Replication is one of the main reasons Kafka can tolerate broker failures.

---

## 1. What is Replication?

Suppose we have:

```text
Partition 0