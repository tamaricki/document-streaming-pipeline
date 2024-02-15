
from kafka import KafkaConsumer

def kafka_consumer():
    consumer = KafkaConsumer('ingestion-topic', group_id='mypythonconsumer', bootstrap_servers='localhost:9092')
    for msg in consumer:
        print(msg)

print('start consuming')

kafka_cocnsumer()

print(done)