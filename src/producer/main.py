import os
import json
import logging
from healthcheck import HealthCheck
from publisher import MessagePublisher
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(level=logging.INFO)
cur_path = os.path.dirname(__file__)

kafka_config = dict()
kafka_config["cafile"] = os.path.join(cur_path,'../certs/ca.pem')
kafka_config["certfile"] = os.path.join(cur_path,'../certs/service.cert')
kafka_config["keyfile"] = os.path.join(cur_path,'../certs/service.key')
kafka_config["host"] = os.getenv('KAFKA_HOST')
kafka_config["port"] = os.getenv('KAFKA_PORT')

producer = MessagePublisher(kafka_config)

website_urls = json.loads(os.getenv('WEBSITES'))

health_check = HealthCheck(producer, website_urls)
health_check.run()