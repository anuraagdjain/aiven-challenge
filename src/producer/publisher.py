from kafka import KafkaProducer
from cloudevents.http import CloudEvent, to_json

class MessagePublisher:
    def __init__(self, config = dict()):
        host = config.get('host')
        port = config.get('port')
        self.kafka_producer = KafkaProducer(
            bootstrap_servers='{}:{}'.format(host, port),
            security_protocol="SSL",
            ssl_cafile=config.get('cafile'),
            ssl_certfile=config.get('certfile'),
            ssl_keyfile=config.get('keyfile'),
        )

    def cloudevents_string(self, value):
        attributes = {
            "type": "com.localhost.healthcheck",
            "source":"healthchecker"
        }
        cloudEvent = CloudEvent(attributes, value)
        return to_json(cloudEvent)
    
    def send(self, topic, payload):
        sanitized_payload = self.cloudevents_string(payload)
        self.kafka_producer.send(topic, sanitized_payload)
        self.kafka_producer.flush()