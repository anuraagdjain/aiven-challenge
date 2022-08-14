import logging
from kafka import KafkaConsumer
import os
from dotenv import load_dotenv
from database import DatabaseSource
from handler import MessageHandler


load_dotenv()
logging.basicConfig(level=logging.INFO)

cur_path = os.path.dirname(__file__)

kafka_config = dict()
kafka_config["cafile"] = os.path.join(cur_path,'../certs/ca.pem')
kafka_config["certfile"] = os.path.join(cur_path,'../certs/service.cert')
kafka_config["keyfile"] = os.path.join(cur_path,'../certs/service.key')
kafka_config["host"] = os.getenv('KAFKA_HOST')
kafka_config["port"] = os.getenv('KAFKA_PORT')


db_config = dict()
db_config["DATABASE_NAME"] = os.getenv('DATABASE_NAME')
db_config["DATABASE_USER"] = os.getenv('DATABASE_USER')
db_config["DATABASE_PASSWORD"] = os.getenv('DATABASE_PASSWORD')
db_config["DATABASE_HOST"] = os.getenv('DATABASE_HOST')
db_config["DATABASE_PORT"] = os.getenv('DATABASE_PORT')


def main():
    try:

        consumer = KafkaConsumer(
            bootstrap_servers='{}:{}'.format(kafka_config["host"], kafka_config["port"]),
            security_protocol="SSL",
            ssl_cafile=kafka_config["cafile"],
            ssl_certfile=kafka_config["certfile"],
            ssl_keyfile=kafka_config["keyfile"],
            auto_offset_reset='earliest'
        )

        consumer.subscribe('services-web-health')

        db = DatabaseSource(db_config)
        messageHandler = MessageHandler(db)
        
        for message in consumer:
    
            logging.info('[main] Incoming message for topic - {}'.format(message.topic))
    
            messageHandler.handle(message.value)
    
    except ValueError as err:
        logging.warn("[Consumer.main] Failed processing message ", err)
    except KeyboardInterrupt:
        logging.info('[Consumer.main] Teardown started')
        
        db.terminate()
        consumer.close()
        
        logging.info('[Consumer.main] Teardown completed')
    except Exception as err:
        logging.warn('[Consumer.main] Unexepected error occurred', err)

if __name__ == "__main__":
    main()
    

