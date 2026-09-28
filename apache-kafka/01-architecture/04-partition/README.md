
---

# 04-partition/README.md

```markdown
# Kafka Partition

A partition is one of the most important concepts in Kafka.

Kafka divides a topic into partitions.

Partitions provide:

- Scalability
- Parallel processing
- Ordering
- Distribution
- Replication

---

## 1. What is a Partition?

A partition is an ordered sequence of records.

Example:

```text
Partition 0

Offset 0 → Record A
Offset 1 → Record B
Offset 2 → Record C
Offset 3 → Record D