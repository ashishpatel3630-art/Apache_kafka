
---

# 7. `diagrams/kafka-architecture.md`

```markdown
# Kafka Architecture

```text
                    +----------------+
                    |    Producer    |
                    +-------+--------+
                            |
                            | Event
                            v
                    +---------------+
                    | Kafka Topic   |
                    +-------+-------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
       +-----------+  +-----------+  +-----------+
       | Consumer A|  | Consumer B|  | Consumer C|
       +-----------+  +-----------+  +-----------+