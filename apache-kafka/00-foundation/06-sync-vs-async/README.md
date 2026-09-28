# 06 — Synchronous vs Asynchronous

Understanding synchronous and asynchronous communication is fundamental to distributed systems, APIs, messaging systems, and event-driven architecture.

---

## What You Will Learn

- Synchronous communication
- Asynchronous communication
- Blocking vs non-blocking
- Request-response model
- Event-driven architecture
- Python examples
- Kafka and asynchronous messaging
- When to use sync vs async

---

# 1. Synchronous Communication

In synchronous communication, the sender waits for the receiver to complete the operation and return a response.

```text
Client
  |
  | Request
  v
Server
  |
  | Processing
  v
Server
  |
  | Response
  v
Client