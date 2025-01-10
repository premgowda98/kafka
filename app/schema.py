from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.error import SchemaRegistryError
import json

schema_json = {
    "type": "object",
    "properties": {
        "firstname": {
            "type": "string"
        }
    }
}

schema_registry = SchemaRegistryClient({"url": "http://localhost:18081"})
topic = "mytopic"

try:
    output = schema_registry.get_latest_version(subject_name=topic)
    print("Schema", output)
except SchemaRegistryError:
    print("No schema Present")
    print("Creating Schema")
    schema = Schema(schema_str=json.dumps(schema_json), schema_type="JSON")
    print("registring schema")
    output = schema_registry.register_schema(subject_name=topic, schema=schema)
    print("Created Schema Registry", output)