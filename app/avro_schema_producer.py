from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField
import json

schema_avro = {
    "type": "record",
    "name": "User",
    "fields": [
        {
            "name": "firstname",
            "type": "string"
        }
    ]
}

conn = {"bootstrap.servers": "localhost:19092"}

producer = Producer(conn)
admin = AdminClient(conn)
schema_registry = SchemaRegistryClient({"url": "http://localhost:18081"})
print(schema_registry.get_latest_version("mytopic-value").schema.schema_str)


topic = "mytopic"
if topic not in  admin.list_topics().topics:
    admin.create_topics([NewTopic(topic, num_partitions=2)])

print("Producer Started")

while True:
    msg = input("Enter the Name: ")
    if msg=="q":
        break

    data = {"firstname": msg}

    avro_serializer = AvroSerializer(schema_registry_client=schema_registry, schema_str=schema_registry.get_latest_version("mytopic-value").schema.schema_str)
    context = SerializationContext(topic=topic, field=MessageField.VALUE)
    serialiased_data = avro_serializer(data, ctx=context)

    print("Sending", serialiased_data)
    producer.produce(topic, serialiased_data)
    producer.flush()