
---

# 6. `diagrams/synchronous.md`

```md
# Synchronous Communication Diagram

## Basic Request-Response

```text
Client
  |
  | Request
  v
Server
  |
  | Processing
  |
  |----------------|
  |     WAIT       |
  |----------------|
  |
  v
Response
  |
  v
Client