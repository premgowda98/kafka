# Kafka Learnings

[Explained](https://www.youtube.com/watch?v=DU8o-OTeoCc&list=PL5q3E8eRUieUHnsz0rh0W6AzwdVJBwEK6&index=1&pp=iAQB)

### **Apache Kafka: Overview and Components**

**Apache Kafka** is an open-source distributed event streaming platform used to handle real-time data feeds. It is designed for high-throughput, fault tolerance, scalability, and low-latency data processing. Kafka is often used for building real-time data pipelines and streaming applications. It allows the publishing, subscribing, storing, and processing of streams of records in a fault-tolerant and scalable manner.

Kafka was originally developed by LinkedIn and later open-sourced as part of the Apache Software Foundation.

### **Key Concepts in Kafka**
Before diving into Kafka's components, it's important to understand a few core concepts:

- **Producer**: A producer sends records (events/messages) to Kafka topics.
- **Consumer**: A consumer reads records from Kafka topics.
- **Broker**: Kafka brokers are the servers that store data and serve client requests (producers and consumers).
- **Topic**: A category or feed name to which records are sent by producers and consumed by consumers.
- **Partition**: Kafka topics are split into partitions for scalability and parallelism. Each partition is an ordered, immutable sequence of records.

---

### **Kafka's Core Components**

1. **Producer**
   - A **Producer** is an application or service that sends records (or events) to a Kafka topic.
   - Producers are responsible for choosing which partition within a topic to send the data. This can be done through round-robin distribution or based on some key that guarantees records with the same key go to the same partition.
   - **Key Functionality**:
     - Write events to topics.
     - Control which partition a record goes to.
     - Optionally, ensure data delivery guarantees (acknowledgments from brokers).
     - Asynchronous message delivery for high throughput.

2. **Consumer**
   - A **Consumer** is an application or service that reads records from one or more Kafka topics.
   - Kafka consumers can be grouped together as part of a **Consumer Group** to horizontally scale the consumption of records. Each consumer in the group reads from a subset of partitions, allowing parallel processing.
   - **Key Functionality**:
     - Read records from Kafka topics.
     - Consumers track their progress using **offsets** (position in the topic/partition).
     - Support for both real-time and batch processing of events.
   
3. **Broker**
   - **Kafka Brokers** are the servers that store and manage Kafka data. Each broker is responsible for managing partitions of topics and serving requests from producers and consumers.
   - Kafka clusters are made up of one or more brokers, and each broker can handle a subset of the partitions of a topic.
   - **Key Functionality**:
     - Handle incoming records from producers.
     - Store records in partitions on disk.
     - Serve requests from consumers.
     - Provide fault tolerance by replicating partitions across multiple brokers.
     - Maintain **Zookeeper** coordination (for older versions of Kafka; newer versions may use internal consensus mechanisms like KRaft).

4. **Topic**
   - A **Topic** is a logical channel to which Kafka producers send messages and from which Kafka consumers read messages.
   - Topics can be split into **partitions** for parallel processing, and each partition is an ordered log of records.
   - **Key Functionality**:
     - Topics allow organizing the event stream into different categories.
     - Each topic can have multiple partitions for horizontal scaling.
   
5. **Partition**
   - A **Partition** is a smaller unit of a topic, enabling Kafka to scale horizontally by distributing records across multiple machines.
   - Each partition is an ordered, immutable sequence of records. Each record within a partition has a unique **offset**.
   - **Key Functionality**:
     - Provides parallelism by distributing records across multiple brokers.
     - Ensures ordering of records within each partition, but not across partitions.
     - Supports horizontal scaling by increasing the number of partitions.
   
6. **Replica**
   - **Replicas** are copies of partitions that are stored on different brokers for fault tolerance.
   - If a broker or partition leader goes down, one of its replicas can take over the leadership role, ensuring data availability.
   - **Key Functionality**:
     - Provides fault tolerance and high availability.
     - Data replication ensures that Kafka remains operational even in the event of broker failure.

7. **Consumer Group**
   - A **Consumer Group** is a group of consumers that work together to consume data from one or more topics.
   - Kafka ensures that each partition of a topic is consumed by only one consumer in the group at any given time.
   - If a consumer fails, another consumer from the group takes over its partitions.
   - **Key Functionality**:
     - Enables **parallel processing** of messages.
     - Each consumer in the group reads from a unique partition of a topic, ensuring high scalability and load balancing.

8. **Zookeeper** (Deprecated in newer versions, replaced by KRaft)
   - **Zookeeper** is used in older versions of Kafka to manage and coordinate Kafka brokers. It helps manage metadata, leader election, and broker synchronization.
   - Zookeeper ensures that brokers in the Kafka cluster are aware of each other's presence and can elect a **partition leader** for each partition in a topic.
   - **Key Functionality**:
     - Coordination of Kafka brokers.
     - Managing metadata for topics, partitions, and consumer offsets.

   **Note**: Newer versions of Kafka (since version 2.8.0) are moving towards **KRaft** (Kafka Raft Protocol), a new internal consensus mechanism that eliminates the dependency on Zookeeper.

9. **Kafka Connect**
   - **Kafka Connect** is a framework for integrating Kafka with other systems, such as databases, data lakes, and external applications.
   - It allows for **data ingestion** into Kafka (source connectors) and **data extraction** from Kafka (sink connectors) using pre-built connectors.
   - **Key Functionality**:
     - Easy integration with external data systems.
     - Supports scaling and fault tolerance for data integration tasks.

10. **Kafka Streams**
    - **Kafka Streams** is a client library for building **real-time, stream processing applications** on top of Kafka.
    - It provides a high-level API for processing streams of data, including filtering, joining, and aggregating data.
    - **Key Functionality**:
      - Real-time processing of Kafka topic data.
      - Enables transformations like **map**, **reduce**, **filter**, and **windowing** on streams.
      - Supports fault tolerance and stateful operations.

11. **Kafka Consumer Offset**
    - **Offsets** represent the position of a consumer in a partition.
    - Kafka allows consumers to commit their offsets, enabling them to resume reading from where they left off in case of failures or restarts.
    - **Key Functionality**:
      - Track consumer progress and handle reprocessing.
      - Offsets can be stored in Kafka itself or an external store.

---

### **How Kafka Works (Flow)**
1. **Producer** sends records to Kafka brokers, publishing to a specific **topic**.
2. Records are stored in **partitions** within the topic. Each record has an **offset** to uniquely identify its position within the partition.
3. **Brokers** handle and store these records on disk and maintain replication for fault tolerance.
4. **Consumers** (or **consumer groups**) read records from topics, typically consuming from multiple partitions for parallel processing.
5. Kafka ensures **data replication**, **fault tolerance**, and **high throughput** while managing the state of each consumer via offsets.

---

### **Kafka Features Summary:**
- **High throughput** and **low latency** for real-time data processing.
- **Scalability** via partitioning and horizontal scaling.
- **Durability** with data replication and retention.
- **Fault tolerance**: Replication ensures availability during broker failures.
- **Horizontal scalability**: Kafka can scale by adding more brokers, partitions, and consumers.
- **Event replayability**: Events can be re-read for stream processing or auditing purposes.
- **Distributed architecture**: It is designed to operate as a distributed, fault-tolerant system.

Kafka is commonly used for applications such as **real-time analytics**, **data pipelines**, **event sourcing**, **log aggregation**, and **stream processing**.

