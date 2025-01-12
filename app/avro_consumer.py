from confluent_kafka import Consumer, KafkaError
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField

group = int(input("Group ID: "))

conn = {"bootstrap.servers": "localhost:19092", "group.id": f"{group}", "auto.offset.reset": "latest"}

consumer = Consumer(conn)
topic = "mytopic"
consumer.subscribe([topic])
schema_registry = SchemaRegistryClient({"url": "http://localhost:18081"})

de_serializer = AvroDeserializer(schema_registry_client=schema_registry, schema_str=schema_registry.get_latest_version("mytopic-value").schema.schema_str)
context = SerializationContext(topic=topic, field=MessageField.VALUE)

print(f"Consumer Started from {group}")

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
            value = msg.value()
            de_serialised_data = de_serializer(value, context)

            print("recieved: ", de_serialised_data)

except KeyboardInterrupt:
    pass
finally:
    # Close the consumer gracefully
    consumer.close()
