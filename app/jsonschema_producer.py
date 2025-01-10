from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField
import json

schema_json = {
    "type": "object",
    "properties": {
        "firstname": {
            "type": "string"
        }
    }
}

conn = {"bootstrap.servers": "localhost:19092"}

producer = Producer(conn)
admin = AdminClient(conn)
schema_registry = SchemaRegistryClient({"url": "http://localhost:18081"})


topic = "mytopic"
if topic not in  admin.list_topics().topics:
    admin.create_topics([NewTopic(topic, num_partitions=2)])

print("Producer Started")

while True:
    msg = input("Enter the Name: ")
    if msg=="q":
        break

    data = {"firstname": msg}

    # The json serializer validaes the input prodvided to the registered schema, but their is one issue
    # json only validates the field types but no the field names, so use AVRO
    json_serializer = JSONSerializer(schema_registry_client=schema_registry, schema_str=json.dumps(schema_json))
    context = SerializationContext(topic=topic, field=MessageField.VALUE)
    serialiased_data = json_serializer(data, ctx=context)

    print("Sending", serialiased_data)
    producer.produce(topic, serialiased_data)
    producer.flush()