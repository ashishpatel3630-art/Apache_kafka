
---

# 8. `diagrams/event-driven.md`

```md
# Event-Driven Architecture

Event-driven architecture is a system design where services communicate by producing and consuming events.

---

# Basic Architecture

```text
Producer
   |
   | Event
   v
Event Broker
   |
   +--------> Consumer A
   |
   +--------> Consumer B
   |
   +--------> Consumer C