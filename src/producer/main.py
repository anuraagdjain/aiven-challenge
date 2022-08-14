import os
import json
import logging
from dotenv import load_dotenv
from repeat_timer import Repeat
from healthcheck import HealthCheck
from publisher import MessagePublisher

load_dotenv()

def main():
    logging.basicConfig(level=logging.INFO)
    cur_path = os.path.dirname(__file__)

    kafka_config = dict()
    kafka_config["cafile"] = os.path.join(cur_path,'../certs/ca.pem')
    kafka_config["certfile"] = os.path.join(cur_path,'../certs/service.cert')
    kafka_config["keyfile"] = os.path.join(cur_path,'../certs/service.key')
    kafka_config["host"] = os.getenv('KAFKA_HOST')
    kafka_config["port"] = os.getenv('KAFKA_PORT')

    refresh_interval =  int(os.getenv('HEALTHCHECK_INTERVAL', 10))
    website_urls = json.loads(os.getenv('WEBSITES'))

    producer = MessagePublisher(kafka_config)
    health_check = HealthCheck(producer, website_urls)
    timer = Repeat(refresh_interval, health_check.run)
    
    try:
        timer.start()
    except KeyboardInterrupt  as err:
        timer.cancel()
        logging.error('[Producer.main] program execution halted - {}'.format(err))


if __name__ == "__main__":
    main()
