
---

# 5. `concepts/comparison.md`

```markdown
# Queue vs Pub/Sub

---

## 1. High-Level Comparison

| Feature | Queue | Pub/Sub |
|---|---|---|
| Communication | Point-to-point | One-to-many |
| Main purpose | Work distribution | Event distribution |
| Consumers | Share work | Independently consume |
| Message handling | Usually one worker handles a job | Multiple subscribers can receive event |
| Typical architecture | Worker system | Event-driven system |
| Kafka implementation | Same consumer group | Different consumer groups |

---

# 2. Queue

```text
Producer
   |
   v
 Queue
   |
   +----> Consumer