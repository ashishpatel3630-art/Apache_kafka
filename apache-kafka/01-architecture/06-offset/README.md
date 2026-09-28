
---

# 06-offset/README.md

```markdown
# Kafka Offset

An offset is a number that identifies the position of a record inside a Kafka partition.

Offsets are one of the most important concepts in Kafka.

---

## 1. What is an Offset?

Example:

```text
Partition 0

Offset 0 → Record A
Offset 1 → Record B
Offset 2 → Record C
Offset 3 → Record D