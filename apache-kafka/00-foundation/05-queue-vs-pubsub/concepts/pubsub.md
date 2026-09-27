
---

# 3. `concepts/pubsub.md`

```markdown
# Publish / Subscribe

Publish/Subscribe, commonly called Pub/Sub, is a messaging pattern where publishers send messages to a topic and multiple subscribers can independently receive those messages.

---

## 1. Basic Architecture

```text
Publisher
    |
    v
  Topic
 /  |  \
v   v   v
A   B   C