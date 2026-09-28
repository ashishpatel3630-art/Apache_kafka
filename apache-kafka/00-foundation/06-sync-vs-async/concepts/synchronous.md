
---

# 2. `concepts/synchronous.md`

```md
# Synchronous Communication

Synchronous communication means that the sender waits for the receiver to complete the operation.

The communication follows a request-response pattern.

---

## Basic Flow

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