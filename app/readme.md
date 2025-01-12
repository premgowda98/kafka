# [Learning Rouse](https://www.youtube.com/playlist?list=PLaNsxqNgctlO5wIfkJhnrXbdUlqxTNoZ5)

# Topic
1. Topic is logical collection of data
2. Can have Partition
3. Can have many Scheam registered to a topic
4. Special Topics
    1. __consumer_offset -> keeps track of messages read by consumers i.e, commited offsets
    2. _schemas -> Used by Schema Registry


# Schema Registry
1. Centralised Repository of schema for the message
2. Associated with Topic

# Producer
1. Pulls Schema -> Serialize Data -> Publish
2. Publishes to the topic


# Consumer
1. Pulls Schema -> Deserialize data -> Process
2. Can have consumer groups
    1. Groups can have many consumers (Instance of same consumer)
    2. If any one consumer in a group has read a message, other conusmers will not read
    3. if 2 partitions are presnet in a Topic, then 2 Consumers can read parallely from 2 partitions
    4. Their is 1 to 1 relation between consumer and partition
    5. If one consumer goes down, then single consumer can consume from 2 partitions
    6. If consumers > partitions then the extra consumer will be hidle
    7. If Producer > Consumer, any one consumer can consume from 2 partition
3. If there are `n` consumer groups, message will be consumed by all consumer groups
4. A new consumer group added will not read the old data
5. If consumer group is down and some message are pushed and then it comes only new messages will be consumed

# Configurations

### Producer Configuration
1. `bootstrap.server`
2. `message.max.bytes`
    1. The max bytes configuration  can be modified at 2 level, one is at producer level and at the topic level
3. `compression.type`
    1. Even for compression type it is the same, but here the topic usually inhertics the compression type of the producer
4. `batch.size`
    1. Here the the message after  serialized they are stored in app buffer and then compress whole batch and then send to kafka
    2. Better optimization
    3. When batch size is reached it is compressed and sent
    4. What if produced only one message and batch size is below the threshold
        1. To overcome this their is one more configuration `linger.ms`
        2. This waits for this milliseconds before sending the messages even if batch size is not met.
5. `cleanup.policy`
    1. 3 types -> delete, compact, compact-delete
    2. When message is sent with same key
        1. with type delete
            1. All the messages will be kept as it is for period set in retention days
        2. with type compact
            1. Only the latest updated data for a key is kept
            2. Also called as **log compaction**
            4. In this type the messages are not deleted even after the retention period is excedded
            5. Their will be always one version of the data
        3. with compact-delete
            1. Combination of delete and compact
            2. After compacted , messages are deleted after retention days
6. **Kafka Tombstone** term used for deleting records
    1. In order to delte a record, message has to be sent with the same *key* that was used for sending messsage but setting value as *None*
    2. This process is called **Tombstone**
    3. Behaves more like a soft delete
7. `partioner`
    1. This helps to send message to a specific partion
    2. It can take 2 values -> random, consistent

### Consumer Configuration

1. `auto.offset.reset`
    1. earliest -> new consumer reads all the historical messages as well
    2. latest -> new consumer reads message only from joined time onwards
    3. none


# Schema Evolution

1. Kroger follows MVC (Major Version Compatability)

### Schema Compatability

1. Backward
    1. Remove Field
    2. Add optional Field
    3. This is default compatiility type in consluent schema registry
    4. Should be compatible with preveious version
    5. New consumer should be able to handle old schema data
    5. Backward Transitive
        1. Should be Compataible with all the previous versions
2. Format
    1. Add Field
    2. Remove optional Field
    3. Old consumer should be able to handle new schema data
3. Full
    1. Add Optional fields
    2. Delete optional fields
4. None


# KCAT (Kafka Command line)