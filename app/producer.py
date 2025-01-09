from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

conn = {"bootstrap.servers": "localhost:19092"}

producer = Producer(conn)
admin = AdminClient(conn)

topic = "mytopic"
if topic not in  admin.list_topics().topics:
    admin.create_topics([NewTopic(topic, num_partitions=2)])

print("Producer Started")

while True:
    msg = input("Enter the message: ")
    if msg=="q":
        break
    producer.produce(topic, msg)
    producer.flush()