
---

# 11-kraft/README.md

```markdown
# KRaft

KRaft stands for:
KRaft is the architecture Kafka uses to manage its own metadata using a Raft-based quorum.

It removes the need for ZooKeeper in modern Kafka deployments.
## 1. What is KRaft?

Older Kafka architecture:

```text
Kafka
  |
  v
ZooKeeper