
---

# 5. `concepts/blocking-vs-nonblocking.md`

```md
# Blocking vs Non-Blocking

Blocking and non-blocking describe whether the current execution flow waits for an operation to complete.

---

# Blocking

In blocking execution, the current thread waits.

```text
Start
  |
  v
Operation
  |
  | WAIT
  |
  v
Result
  |
  v
Continue