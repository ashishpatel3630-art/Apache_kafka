
---

# 3. `concepts/asynchronous.md`

```md
# Asynchronous Communication

Asynchronous communication allows a sender to send a message without waiting for the receiver to finish processing it.

---

# Basic Flow

```text
Producer
   |
   | Message
   v
Queue / Kafka
   |
   v
Consumer