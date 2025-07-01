# Apache Kafka: Topics, Partitions, and Consumer Group Behavior

## 1. Kafka Topics and Partitions: Overview

### Topic:

A **Kafka topic** is a category or feed name to which records are sent. Think of it as a log file where messages are appended.

### Partition:

A **partition** is a **sub-log** or **shard** of a topic. Every topic in Kafka is split into one or more partitions. Each partition is an **ordered, immutable sequence** of records.

* Partitions provide **parallelism**.
* Each partition is **replicated** for fault-tolerance.
* Each message within a partition has a unique **offset**.

### Diagram: Topic with 3 Partitions

```
Topic: user-events

  Partition 0: [msg1, msg4, msg7, ...]
  Partition 1: [msg2, msg5, msg8, ...]
  Partition 2: [msg3, msg6, msg9, ...]
```

## 2. How Messages Are Assigned to Partitions

Kafka producers determine which partition a message goes to, using:

1. **Keyed messages**: The key is hashed, and the hash determines the partition.
2. **No key**: Kafka uses a round-robin approach across partitions.

### Example:

```go
producer.send(topic="user-events", key="user123", value="login")
```

If "user123" hashes to partition 1, the message is appended to partition 1.

## 3. Kafka Consumer Group Model

* A **consumer group** is a set of consumers working together to consume messages from a topic.
* Each **partition** is assigned to **only one consumer** in a group at any time.
* A **consumer can have multiple partitions**.
* Kafka ensures **ordering** within a partition.

### Case 1: More Partitions than Consumers

```
Partitions: P0, P1, P2, P3, P4, P5
Consumers:  C0, C1, C2

Assignments:
C0 -> P0, P3
C1 -> P1, P4
C2 -> P2, P5
```

### Case 2: More Consumers than Partitions

```
Partitions: P0, P1, P2
Consumers:  C0, C1, C2, C3

Assignments:
C0 -> P0
C1 -> P1
C2 -> P2
C3 -> idle (no partition assigned)
```

## 4. Rebalancing and Partition Movement

Rebalancing happens when:

* A consumer joins or leaves the group.
* A consumer fails (no heartbeats within `session.timeout.ms`).
* Partitions are added to a topic.

During rebalancing, Kafka redistributes partitions **evenly** among available consumers.

### Important Configs:

* `session.timeout.ms`: Time to detect consumer failure
* `max.poll.interval.ms`: Max time allowed between polls (to detect slow consumers)

## 5. Duplicate Processing and Rebalance Caveats

If a consumer fetches a message and doesn’t commit before a rebalance:

* The same message will be delivered to another consumer (from last committed offset).
* If both consumers succeed → duplicate side-effects.

### At-least-once Semantics:

* Kafka guarantees messages are delivered **at least once**, not **exactly once**.

### Prevention Tips:

* Use idempotent processing logic
* Tune `max.poll.interval.ms`
* Use manual commits (`enable.auto.commit = false`)

## 6. Summary Table

| Scenario                        | Behavior                                 |
| ------------------------------- | ---------------------------------------- |
| More partitions than consumers  | Some consumers get multiple partitions   |
| More consumers than partitions  | Some consumers are idle                  |
| Consumer dies                   | Partitions reassigned to others          |
| Consumer slow (no poll)         | Rebalance after `max.poll.interval.ms`   |
| Consumer stops heartbeat        | Rebalance after `session.timeout.ms`     |
| Uncommitted message after crash | Message re-delivered to another consumer |

## 7. Final Diagram

```
           Topic: orders (6 partitions)

  P0 ─────────► C0
  P1 ─────────► C0
  P2 ─────────► C1
  P3 ─────────► C1
  P4 ─────────► C2
  P5 ─────────► C2

  (Consumers in same group: "order-group")
  (All partitions actively consumed)
```

---

This note summarizes the core concepts and caveats around Kafka **topics, partitions, and consumer behavior**.
Let me know if you'd like an illustrated PDF version or code samples in Go/Python for producers and consumers.
