from confluent_kafka import Consumer, KafkaError

conn = {"bootstrap.servers": "localhost:19092", "group.id": "1"}

consumer = Consumer(conn)
topic = "mytopic"
consumer.subscribe([topic])

print("Consumer Started")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f'Error while consuming: {msg.error()}')
        else:
            # Parse the received message
            value = msg.value().decode('utf-8')
            print("recieved: ", value)

except KeyboardInterrupt:
    pass
finally:
    # Close the consumer gracefully
    consumer.close()
